import pytest
from app.db.models import ChatHistory

def test_chat_history_model():
    """Test ChatHistory model basic functionality."""
    message = ChatHistory(
        session_id="test_session",
        role="user",
        content="Test message"
    )
    
    assert message.session_id == "test_session"
    assert message.role == "user"
    assert message.content == "Test message"
    assert "ChatHistory" in repr(message)

@pytest.mark.asyncio
async def test_tickets_handler():
    """Test tickets handler functionality."""
    from app.handlers.tickets_handler import obter_resumo_com_personagem
    
    resultado = await obter_resumo_com_personagem(123)
    
    assert resultado["cliente_id"] == 123
    assert resultado["personagem"] == "Capitão IA"
    assert "123" in resultado["mensagem"]