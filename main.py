from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Modelo de dados
class Mensagem(BaseModel):
    conteudo: str

# Banco de dados em memória
mensagens = {}
id_atual = 0

# Criar mensagem
@app.post("/mensagens")
def criar_mensagem(mensagem: Mensagem):
    global id_atual
    id_atual += 1
    mensagens[id_atual] = mensagem.conteudo
    return {"id": id_atual, "conteudo": mensagem.conteudo}

# Listar todas
@app.get("/mensagens")
def listar_mensagens():
    return [{"id": id, "conteudo": conteudo} for id, conteudo in mensagens.items()]

# Obter uma mensagem
@app.get("/mensagens/{id}")
def obter_mensagem(id: int):
    if id not in mensagens:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return {"id": id, "conteudo": mensagens[id]}

# Atualizar mensagem
@app.put("/mensagens/{id}")
def atualizar_mensagem(id: int, nova_mensagem: Mensagem):
    if id not in mensagens:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    mensagens[id] = nova_mensagem.conteudo
    return {"id": id, "conteudo": nova_mensagem.conteudo}

# Deletar mensagem
@app.delete("/mensagens/{id}")
def deletar_mensagem(id: int):
    if id not in mensagens:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    del mensagens[id]
    return {"mensagem": "Mensagem deletada com sucesso"}
