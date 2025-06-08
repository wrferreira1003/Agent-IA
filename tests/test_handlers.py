import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.handlers.pergunta_handler import processar_pergunta
from app.handlers.tickets_handler import obter_resumo_com_personagem
from app.db.models import ChatHistory

@pytest.mark.asyncio
async def test_obter_resumo_com_personagem():
    """Test tickets handler function."""
    cliente_id = 123
    resultado = await obter_resumo_com_personagem(cliente_id)
    
    assert resultado["cliente_id"] == cliente_id
    assert resultado["personagem"] == "Capitão IA"
    assert "123" in resultado["mensagem"]
    assert resultado["tipo"] == "resumo_inicial"

@pytest.mark.asyncio
async def test_processar_pergunta_with_mock_db():
    """Test pergunta handler with mocked dependencies."""
    cliente_id = 123
    pergunta = "Qual é o status do meu ticket?"
    
    # Mock do banco de dados
    mock_db = Mock()
    mock_db.execute = AsyncMock()
    mock_db.add = Mock()
    mock_db.commit = AsyncMock()
    
    # Mock do resultado da query
    mock_result = Mock()
    mock_result.scalars.return_value.all.return_value = []
    mock_db.execute.return_value = mock_result
    
    # Mock do agent
    mock_agent = Mock()
    mock_agent.get_response = AsyncMock(return_value="Resposta do agente")
    
    with patch('app.handlers.pergunta_handler.get_db') as mock_get_db, \
         patch('app.handlers.pergunta_handler.ChatAgent') as mock_chat_agent:
        
        # Configurar mocks
        async def mock_db_generator():
            yield mock_db
        
        mock_get_db.return_value = mock_db_generator()
        mock_chat_agent.return_value = mock_agent
        
        # Executar função
        resultado = await processar_pergunta(cliente_id, pergunta)
        
        # Verificações
        assert resultado == "Resposta do agente"
        mock_db.execute.assert_called_once()
        assert mock_db.add.call_count == 2  # pergunta + resposta
        mock_db.commit.assert_called_once()
        mock_agent.get_response.assert_called_once_with(pergunta)