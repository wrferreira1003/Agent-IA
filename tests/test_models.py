import pytest
from app.db.models import ChatHistory
from sqlalchemy import select
import uuid

@pytest.mark.asyncio
async def test_chat_history_creation(async_session):
    """Test ChatHistory model creation."""
    # Criar uma nova mensagem
    message = ChatHistory(
        session_id="test_session_123",
        role="user",
        content="Olá, como você está?"
    )
    
    async_session.add(message)
    await async_session.commit()
    
    # Verificar se foi salvo corretamente
    result = await async_session.execute(
        select(ChatHistory).where(ChatHistory.session_id == "test_session_123")
    )
    saved_message = result.scalar_one()
    
    assert saved_message.session_id == "test_session_123"
    assert saved_message.role == "user"
    assert saved_message.content == "Olá, como você está?"
    assert saved_message.created_at is not None
    assert isinstance(saved_message.id, uuid.UUID)

@pytest.mark.asyncio
async def test_chat_history_multiple_messages(async_session):
    """Test storing multiple messages for a session."""
    session_id = "test_session_456"
    
    # Criar múltiplas mensagens
    messages = [
        ChatHistory(session_id=session_id, role="user", content="Primeira pergunta"),
        ChatHistory(session_id=session_id, role="model", content="Primeira resposta"),
        ChatHistory(session_id=session_id, role="user", content="Segunda pergunta"),
    ]
    
    for msg in messages:
        async_session.add(msg)
    await async_session.commit()
    
    # Verificar se todas foram salvas
    result = await async_session.execute(
        select(ChatHistory)
        .where(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.created_at)
    )
    saved_messages = result.scalars().all()
    
    assert len(saved_messages) == 3
    assert saved_messages[0].role == "user"
    assert saved_messages[1].role == "model"
    assert saved_messages[2].role == "user"

@pytest.mark.asyncio
async def test_chat_history_repr(async_session):
    """Test ChatHistory __repr__ method."""
    message = ChatHistory(
        session_id="test_repr",
        role="user",
        content="Test message"
    )
    
    repr_str = repr(message)
    assert "ChatHistory" in repr_str
    assert "test_repr" in repr_str
    assert "user" in repr_str