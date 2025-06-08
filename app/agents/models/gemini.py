import google.generativeai as genai
from app.core.config import settings
from app.agents.tools.notion_tools import available_tools

# Configura a API Key do Google
genai.configure(api_key=settings.GOOGLE_API_KEY)

class GeminiModel:
    """
    Wrapper para o modelo generativo do Google (Gemini).
    """
    def __init__(self, model_name: str = settings.GEMINI_MODEL_NAME):
        # Usar as ferramentas diretamente (forma simples do SDK)
        self.tools = available_tools
        print(f"🔧 Ferramentas registradas no Gemini: {len(self.tools)}")
        for tool in self.tools:
            print(f"  - {tool.__name__}: {tool.__doc__}")
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=self.tools,
            system_instruction="""Você é o Capitão IA, um assistente prestativo que tem acesso a documentos do Notion.

IMPORTANTE: Quando perguntarem sobre documentos, projetos ou informações específicas, use as ferramentas disponíveis:

- Para ver informações dos documentos → use search_notion_pages()
- Para criar nova página → use create_notion_page()

Você tem acesso a uma página sobre "REST API's com Django Ninja" no Notion.
Use as ferramentas sempre que apropriado para responder com informações reais."""
        )

    def start_chat(self, history: list = None):
        """
        Inicia uma sessão de chat, opcionalmente com um histórico de conversas.
        History deve ser uma lista de dicionários: [{'role': 'user'/'model', 'parts': [text]}]
        """
        if history is None:
            history = []
        return self.model.start_chat(history=history)