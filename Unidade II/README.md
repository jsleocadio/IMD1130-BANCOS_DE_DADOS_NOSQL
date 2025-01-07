# IMD1130-BANCOS_DE_DADOS_NOSQL

## Descrição do Projeto

Este projeto é uma API desenvolvida com FastAPI que interage com um banco de dados MongoDB. A API permite criar, recuperar, atualizar documentos em coleções específicas do MongoDB.

## Estrutura do Projeto

- `api/`: Contém o código da API.
    - `app.py`: Código principal da API.
    - `requirements.txt`: Dependências do projeto.
    - `Dockerfile`: Dockerfile para construir a imagem da API.
- `mongodb/`: Contém o Dockerfile para o MongoDB.
    - `Dockerfile`: Dockerfile para construir a imagem do MongoDB.
- `docker-compose.yml`: Arquivo de configuração do Docker Compose.
- `start`: Script para iniciar os serviços Docker.
- `stop`: Script para parar os serviços Docker.

## Pré-requisitos

- Docker
- Docker Compose

## Como Executar o Projeto

1. Clone o repositório:
     ```bash
     git clone https://github.com/jsleocadio/IMD1130-BANCOS_DE_DADOS_NOSQL.git
     cd IMD1130-BANCOS_DE_DADOS_NOSQL/Unidade\ II/
     ```

2. Inicie os serviços Docker:
     ```bash
     ./start
     ```

3. Acesse a API em `http://localhost:8888`.

## Endpoints da API

### Criar um novo documento

- **POST** `/{collection_name}`
- **Descrição**: Cria um novo documento na coleção especificada.
- **Parâmetros**:
    - `collection_name` (path): Nome da coleção.
    - `document` (body): Documento a ser criado.

### Recuperar todos os documentos

- **GET** `/{collection_name}`
- **Descrição**: Recupera todos os documentos da coleção especificada.
- **Parâmetros**:
    - `collection_name` (path): Nome da coleção.
    - `query` (query): Filtro de consulta (opcional).
    ```
    /{nome_da_coleção}?query={"name":"Bob"}
    /{nome_da_coleção}?query={"name":{"$regex":"/Bo$/"}}
    /{nome_da_coleção}?query={"age":{"$gt":12}}
    /{nome_da_coleção}?query={"age":{"$gte":12}}
    ```
    - `fields` (query): Campos a serem retornados (opcional).
     ```
    /{nome_da_coleção}?fields=name #Exibirá apenas name
    /{nome_da_coleção}?fields=-name #Não exibirá name
    /{nome_da_coleção}?fields=name,age #Exibirá name e age
    ```
    - `skip` (query): Número de documentos a pular (opcional).
    - `limit` (query): Número máximo de documentos a retornar (opcional).

### Recuperar um documento por ID

- **GET** `/{collection_name}/{doc_id}`
- **Descrição**: Recupera um documento pelo ID na coleção especificada.
- **Parâmetros**:
    - `collection_name` (path): Nome da coleção.
    - `doc_id` (path): ID do documento.

### Atualizar um documento por ID

- **PUT** `/{collection_name}/{doc_id}`
- **Descrição**: Atualiza um documento pelo ID na coleção especificada.
- **Parâmetros**:
    - `collection_name` (path): Nome da coleção.
    - `doc_id` (path): ID do documento.
    - `document` (body): Documento atualizado.

## Parar os Serviços

Para parar os serviços Docker, execute:
```bash
./stop
```

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](../LICENSE) para mais detalhes.