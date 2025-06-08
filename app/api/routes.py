from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.handlers.pergunta_handler import processar_pergunta
from app.handlers.tickets_handler import obter_resumo_com_personagem

router = APIRouter()

class PerguntaPayload(BaseModel):
    cliente_id: int
    pergunta: str

@router.post("/perguntar")
async def perguntar(payload: PerguntaPayload):
    resposta = await processar_pergunta(payload.cliente_id, payload.pergunta)
    return {"resposta": resposta}

@router.get("/resumo_tickets")
async def resumo_tickets(cliente_id: int):
    resumo = await obter_resumo_com_personagem(cliente_id)
    return resumo