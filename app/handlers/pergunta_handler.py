
from app.agents.main_agent import ChatAgent
from app.db.models import ChatHistory
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

async def processar_pergunta(cliente_id: int, pergunta: str) -> str:
    async for db in get_db():
        # Recuperar histórico da conversa
        result = await db.execute(
            select(ChatHistory)
            .where(ChatHistory.session_id == str(cliente_id))
            .order_by(ChatHistory.created_at.desc())
            .limit(10)
        )
        historico = result.scalars().all()
        
        # Converter para formato Gemini
        history = []
        for msg in reversed(historico):
            history.append({
                'role': msg.role,
                'parts': [msg.content]
            })
        
        # Processar com o agente
        agent = ChatAgent(history=history)
        resposta = await agent.get_response(pergunta)
        
        # Salvar pergunta do usuário
        nova_pergunta = ChatHistory(
            session_id=str(cliente_id),
            role="user",
            content=pergunta
        )
        db.add(nova_pergunta)
        
        # Salvar resposta do modelo
        nova_resposta = ChatHistory(
            session_id=str(cliente_id),
            role="model",
            content=resposta
        )
        db.add(nova_resposta)
        
        await db.commit()
        return resposta