# API Mensagens

API RESTful simples para gerenciamento de mensagens (CRUD), desenvolvida com FastAPI.

## Como executar no GitHub Codespaces

1. Abra o Codespaces no repositório.
2. Instale as dependências:
    pip install -r requirements.txt
3. Execute a API:
4. Copie a URL pública exibida e utilize no Postman.

## Rotas da API

- POST `/mensagens` – Criar nova mensagem
- GET `/mensagens` – Listar todas as mensagens
- GET `/mensagens/{id}` – Obter uma mensagem
- PUT `/mensagens/{id}` – Atualizar mensagem
- DELETE `/mensagens/{id}` – Deletar mensagem
