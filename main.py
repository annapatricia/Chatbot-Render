from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI(title="Chatbot com Guardrails + RAG")

# ======================
# Base de conhecimento (RAG)
# ======================

DOCUMENTOS = [
    "O Itaú oferece crédito pessoal com taxas variáveis conforme o perfil do cliente.",
    "Para abrir uma conta PJ no Itaú, são necessários contrato social e CNPJ.",
    "O atendimento digital do Itaú funciona 24 horas por dia."
]

# ======================
# MODELO DE ENTRADA
# ======================

class Mensagem(BaseModel):
    mensagem: str

# ======================
# RETRIEVER (RAG)
# ======================

def recuperar_documentos(pergunta: str):
    resultados = []
    for doc in DOCUMENTOS:
        if any(p.lower() in doc.lower() for p in pergunta.split()):
            resultados.append(doc)
    return resultados

# ======================
# ORQUESTRADOR DE PROMPT
# ======================

def montar_prompt(pergunta: str, docs):
    contexto = "\n".join(docs)
    return f"""
Você é um assistente financeiro do Itaú.
Responda apenas com base nas informações abaixo.

Informações:
{contexto}

Pergunta:
{pergunta}
"""

# ======================
# LLM SIMULADO
# ======================

def llm_simulado(prompt: str):
    return "Resposta baseada nas informações recuperadas."

# ======================
# ENDPOINT CHAT
# ======================

@app.post("/chat")
def chat(m: Mensagem):
    docs = recuperar_documentos(m.mensagem)

    if not docs:
        raise HTTPException(
            status_code=404,
            detail="Não encontrei informações suficientes para responder."
        )

    prompt = montar_prompt(m.mensagem, docs)
    resposta = llm_simulado(prompt)

    return {
        "resposta": resposta,
        "fontes": docs
    }

# ======================
# STATUS
# ======================

@app.get("/status")
def status():
    return {"status": "Chatbot RAG ativo no Render"}
