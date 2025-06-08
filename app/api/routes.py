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

@router.get("/test_notion")
async def test_notion():
    """Endpoint para testar diretamente a conexão com Notion"""
    from app.agents.tools.notion_tools import read_notion_page
    result = read_notion_page()
    return {"notion_test": result}

@router.get("/test_agent_tools")
async def test_agent_tools():
    """Endpoint para testar se o agente usa as ferramentas"""
    from app.agents.main_agent import ChatAgent
    
    # Simular uma função de busca que funciona
    def mock_search():
        return """📄 Página do Notion: Projeto PETCOMPARA APP
🔗 URL: https://www.notion.so/Projeto-PETCOMPARA-APP-79508c00b6324c9bbecd7ff2dcc7db4a
📅 Criado: 2024-01-15
✏️ Última edição: 2024-06-08
📝 Blocos encontrados: 25

📋 Conteúdo:
# Projeto PETCOMPARA APP
## Visão Geral
O PETCOMPARA é uma aplicação inovadora para comparação de preços de produtos pet.
## Funcionalidades Principais
• Comparação de preços em tempo real
• Catálogo de produtos para pets
• Sistema de avaliações e reviews
• Integração com principais lojas
## Tecnologias
• Backend: Python/FastAPI
• Frontend: React Native
• Banco de dados: PostgreSQL
• Deploy: Docker/AWS"""
    
    # Temporariamente substituir a função real
    import app.agents.tools.notion_tools as notion_tools
    original_func = notion_tools.read_notion_page
    notion_tools.read_notion_page = mock_search
    
    try:
        agent = ChatAgent()
        response = await agent.get_response("O que você sabe sobre PETCOMPARA?")
        return {"agent_response": response, "test": "com_notion_simulado"}
    finally:
        # Restaurar função original
        notion_tools.read_notion_page = original_func