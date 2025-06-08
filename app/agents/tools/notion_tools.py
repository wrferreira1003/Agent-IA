import notion_client
from app.core.config import settings
import google.generativeai as genai

# Caso a biblioteca do Google não esteja instalada (ex.: ambiente de testes),
# definimos decoradores "fake" para evitar erros de importação.
try:
    tool_decorator = genai.tools.text  # Decorador oficial para funções de texto
except Exception:  # pragma: no cover - fallback para ambientes sem a lib
    class _DummyDecorator:  # simples no-op
        def __call__(self, func):
            return func

    tool_decorator = _DummyDecorator()

# Inicializa o cliente do Notion de forma síncrona
# Para uso em um ambiente assíncrono, considere rodar em um executor de thread
notion = notion_client.Client(auth=settings.NOTION_API_KEY)

def create_notion_page_impl(title: str, content: str) -> str:
    """
    Implementação da criação de página no Notion como filha da página principal.
    """
    try:
        response = notion.pages.create(
            parent={"page_id": settings.NOTION_DATABASE_ID},
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
        return f"Falha ao criar a página no Notion: {e}"

def read_notion_page() -> str:
    """
    Lê o conteúdo da página específica do Notion (Projeto PETCOMPARA APP).
    """
    try:
        # Obter informações da página
        page_response = notion.pages.retrieve(page_id=settings.NOTION_DATABASE_ID)
        
        # Extrair título da página
        title = "REST API's com Django Ninja"
        page_url = page_response.get("url", "")
        created_time = page_response.get("created_time", "")
        last_edited_time = page_response.get("last_edited_time", "")
        
        # Obter conteúdo da página (blocos)
        blocks_response = notion.blocks.children.list(
            block_id=settings.NOTION_DATABASE_ID,
            page_size=50
        )
        blocks = blocks_response.get("results", [])
        
        # Processar conteúdo
        content_sections = []
        
        for block in blocks:
            block_type = block.get("type")
            
            if block_type == "paragraph":
                rich_text = block.get("paragraph", {}).get("rich_text", [])
                text = "".join([rt.get("plain_text", "") for rt in rich_text])
                if text.strip():
                    content_sections.append(f"Parágrafo: {text}")
            
            elif block_type == "heading_1":
                rich_text = block.get("heading_1", {}).get("rich_text", [])
                text = "".join([rt.get("plain_text", "") for rt in rich_text])
                if text.strip():
                    content_sections.append(f"# {text}")
            
            elif block_type == "heading_2":
                rich_text = block.get("heading_2", {}).get("rich_text", [])
                text = "".join([rt.get("plain_text", "") for rt in rich_text])
                if text.strip():
                    content_sections.append(f"## {text}")
            
            elif block_type == "heading_3":
                rich_text = block.get("heading_3", {}).get("rich_text", [])
                text = "".join([rt.get("plain_text", "") for rt in rich_text])
                if text.strip():
                    content_sections.append(f"### {text}")
            
            elif block_type == "bulleted_list_item":
                rich_text = block.get("bulleted_list_item", {}).get("rich_text", [])
                text = "".join([rt.get("plain_text", "") for rt in rich_text])
                if text.strip():
                    content_sections.append(f"• {text}")
            
            elif block_type == "numbered_list_item":
                rich_text = block.get("numbered_list_item", {}).get("rich_text", [])
                text = "".join([rt.get("plain_text", "") for rt in rich_text])
                if text.strip():
                    content_sections.append(f"1. {text}")
        
        # Montar resultado
        result = f"📄 Página do Notion: {title}\n"
        result += f"🔗 URL: {page_url}\n"
        result += f"📅 Criado: {created_time[:10] if created_time else 'N/A'}\n"
        result += f"✏️ Última edição: {last_edited_time[:10] if last_edited_time else 'N/A'}\n"
        result += f"📝 Blocos encontrados: {len(blocks)}\n\n"
        
        if content_sections:
            result += "📋 Conteúdo:\n" + "\n".join(content_sections[:20])  # Primeiros 20 itens
            if len(content_sections) > 20:
                result += f"\n... e mais {len(content_sections) - 20} seções"
        else:
            result += "📋 Conteúdo: Página vazia ou sem conteúdo legível"
        
        return result
        
    except Exception as e:
        return f"❌ Erro ao acessar a página do Notion: {e}\n\n" \
               f"💡 Certifique-se de que:\n" \
               f"1. A integração 'Capitão IA' foi adicionada à página\n" \
               f"2. As permissões foram definidas como 'Full access' ou 'Edit'\n" \
               f"3. A página está acessível: https://www.notion.so/REST-API-s-com-Django-Ninja-f75599ed25fa404dac7b7ae4ba84830b"

@tool_decorator
def create_notion_page(title: str, content: str) -> str:
    """
    Cria uma nova página em um banco de dados específico do Notion.

    Args:
        title: O título da nova página do Notion
        content: O conteúdo principal a ser adicionado no corpo da página

    Returns:
        A URL da página criada ou uma mensagem de erro
    """
    return create_notion_page_impl(title, content)

@tool_decorator
def search_notion_pages() -> str:
    """
    Lê e exibe o conteúdo da página do Notion (REST API's com Django Ninja).

    Returns:
        Conteúdo detalhado da página com títulos, parágrafos e listas
    """
    return read_notion_page()

# Definir ferramentas diretamente para o Gemini (forma simples)
available_tools = [create_notion_page, search_notion_pages]