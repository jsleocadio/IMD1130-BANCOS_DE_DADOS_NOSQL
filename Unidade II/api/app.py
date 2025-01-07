from fastapi import FastAPI, HTTPException, Query, Path
from pymongo import MongoClient
from bson import ObjectId
import os
import json
import logging

app = FastAPI()

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da conexão com o MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["mydatabase"]

def parse_projection(fields: str):
    """
    Converte uma string de campos para um dicionário de projeção.
    
    Args:
        fields (str): String de campos separados por vírgula.
        
    Returns:
        dict: Dicionário de projeção.
    """
    projection = {}
    if fields:
        for field in fields.split(","):
            field = field.strip()
            if field.startswith("-"):
                projection[field[1:]] = 0
            else:
                projection[field] = 1
    return projection

def convert_objectid(doc):
    """
    Converte um documento do MongoDB para um formato JSON serializável.
    """
    if isinstance(doc, dict):
        return {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in doc.items()}
    return doc

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/{collection_name}", summary="Retrieve all documents", description="Retrieve all documents from the database")
def get_docs(
    collection_name: str = Path(..., description="Name of the collection to retrieve"),
    query: str = Query("{}", description="Query string to filter users"),
    fields: str = Query(None, description="Fields to return in the response"),
    skip: int = 0,
    limit: int = 10):
    logger.info(f"Retrieving documents from collection: {collection_name}...")
    try:
        collection = db[collection_name]
        # Converte o parâmetro query de string para dicionário
        query_dict = json.loads(query)

        # Converte a string de campos para um dicionário de projeção
        projection = parse_projection(fields)
        
        # Busca no MongoDB aplicando o filtro
        documents = list(collection.find(query_dict, projection).skip(skip).limit(limit))

        # Converte os documentos do MongoDB para um formato JSON serializável
        documents = [convert_objectid(doc) for doc in documents]
        
        # Retorna os resultados e informações de paginação
        return {
            "documents": documents,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "count": len(documents)
            }
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid query format. Must be a valid JSON string.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/{collection_name}/{doc_id}", summary="Retrieve a document", description="Retrieve a document by its ID")
def get_document(
    collection_name: str = Path(..., description="Name of the collection to retrieve"),
    doc_id: int = None):
    logger.info(f"Searching for user with ID {doc_id}...")
    try:
        collection = db[collection_name]
        document = collection.find_one({"_id": doc_id}, {"_id": 0})

        if document:
            logger.info(f"Document found: {document}")
            return document
        else:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="Document not found")
    except ValueError:
        logger.error("Invalid ID")
        raise HTTPException(status_code=400, detail="Invalid document ID format")

@app.post("/{collection_name}", summary="Create a new document", description="Create a new document in the database")
def create_document(
    collection_name: str = Path(..., description="Name of the collection to create"),
    document: dict = None):
    logger.info(f"Creating a new document in collection: {collection_name}...")
    try:
        collection = db[collection_name]
        # Busca o registro com o maior 'id'
        max_id_record = collection.find_one(sort=[("_id", -1)])
        next_id = (max_id_record["_id"] + 1) if max_id_record and isinstance(max_id_record["_id"], int) else 1

        # Adiciona o ID ao novo registro
        if "_id" not in document:
            document["_id"] = next_id

        # Insere o registro no MongoDB
        result = collection.insert_one(document)

        if result.inserted_id:
            logger.info(f"Document created successfully: {document}")
            return {"message": "Record added successfully", "document": convert_objectid(document)}
        else:
            logger.error("Failed to add document")
            raise HTTPException(status_code=500, detail="Failed to add document")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.put("/{collection_name}/{doc_id}", summary="Update a document", description="Update a document by its ID")
def update_user(
    collection_name: str = Path(..., description="Name of the collection to update"),
    doc_id: int = None,
    document: dict = None):
    logger.info(f"Updating document with ID {doc_id}...")
    try:
        collection = db[collection_name]
        # Atualiza o registro no MongoDB
        result = collection.update_one({"_id": doc_id}, {"$set": document})

        if result.modified_count > 0:
            logger.info(f"Document updated successfully: {document}")
            return {"message": "Document updated successfully", "document": document}
        else:
            logger.error("Failed to document record")
            raise HTTPException(status_code=404, detail="Document not found")
    except ValueError:
        logger.error("Invalid ID")
        raise HTTPException(status_code=400, detail="Invalid document ID format")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
