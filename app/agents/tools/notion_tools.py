import notion_client
from app.core.config import settings

# Inicializa o cliente do Notion de forma síncrona
# Para uso em um ambiente assíncrono, considere rodar em um executor de thread
notion = notion_client.Client(auth=settings.NOTION_API_KEY)

def create_notion_page(title: str, content: str) -> str:
    """
    Cria uma nova página em um banco de dados específico do Notion.

    Args:
        title (str): O título da nova página do Notion.
        content (str): O conteúdo principal a ser adicionado no corpo da página.

    Returns:
        str: A URL da página criada ou uma mensagem de erro.
    """
    try:
        response = notion.pages.create(
            parent={"database_id": settings.NOTION_DATABASE_ID},
            properties={
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            },
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": content}}]
                    }
                }
            ]
        )
        page_url = response.get("url")
        return f"Página criada com sucesso no Notion: {page_url}"
    except Exception as e:
        # Idealmente, logar o erro aqui
        return f"Falha ao criar a página no Notion: {e}"

# Lista de ferramentas para o agente
available_tools = {
    "create_notion_page": create_notion_page,
}