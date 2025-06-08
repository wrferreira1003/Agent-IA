import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_root_endpoint(async_client):
    """Test root endpoint."""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Capitão IA"}

@pytest.mark.asyncio
async def test_perguntar_endpoint(async_client):
    """Test perguntar endpoint."""
    with patch('app.handlers.pergunta_handler.processar_pergunta') as mock_processar:
        mock_processar.return_value = "Resposta do teste"
        
        payload = {
            "cliente_id": 123,
            "pergunta": "Como está o tempo?"
        }
        
        response = await async_client.post("/api/v1/perguntar", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["resposta"] == "Resposta do teste"
        mock_processar.assert_called_once_with(123, "Como está o tempo?")

@pytest.mark.asyncio
async def test_resumo_tickets_endpoint(async_client):
    """Test resumo tickets endpoint."""
    with patch('app.handlers.tickets_handler.obter_resumo_com_personagem') as mock_resumo:
        mock_resumo.return_value = {
            "cliente_id": 456,
            "personagem": "Capitão IA",
            "mensagem": "Resumo de teste",
            "tipo": "resumo_inicial"
        }
        
        response = await async_client.get("/api/v1/resumo_tickets?cliente_id=456")
        
        assert response.status_code == 200
        data = response.json()
        assert data["cliente_id"] == 456
        assert data["personagem"] == "Capitão IA"
        mock_resumo.assert_called_once_with(456)

@pytest.mark.asyncio
async def test_perguntar_endpoint_validation_error(async_client):
    """Test perguntar endpoint with invalid payload."""
    payload = {
        "cliente_id": "invalid",  # Should be int
        "pergunta": "Test question"
    }
    
    response = await async_client.post("/api/v1/perguntar", json=payload)
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_resumo_tickets_missing_parameter(async_client):
    """Test resumo tickets endpoint without cliente_id."""
    response = await async_client.get("/api/v1/resumo_tickets")
    assert response.status_code == 422  # Missing required parameter