# app/api/v1/endpoints.py
from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.agents.main_agent import ChatAgent
# Funções de DB a serem criadas
# from app.db.crud import get_chat_history, save_chat_message 

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para interagir com o agente de IA.
    """
    # 1. Recuperar histórico do banco de dados (a ser implementado)
    # history = await get_chat_history(db, session_id=request.session_id)
    history = [] # Placeholder por enquanto

    # 2. Inicializar o agente com o histórico
    agent = ChatAgent(history=history)

    # 3. Obter a resposta do agente
    agent_response = await agent.get_response(request.message)

    # 4. Salvar a interação no banco de dados (a ser implementado)
    # await save_chat_message(db, session_id=request.session_id, role="user", content=request.message)
    # await save_chat_message(db, session_id=request.session_id, role="model", content=agent_response)

    return ChatResponse(response=agent_response)