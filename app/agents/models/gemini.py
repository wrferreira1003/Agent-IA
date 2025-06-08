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
        # Converte as funções Python em ferramentas para o Gemini
        self.tools = list(available_tools.values())
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=self.tools,
            system_instruction="Você é um assistente prestativo que pode usar ferramentas para interagir com outros serviços, como o Notion."
        )

    def start_chat(self, history: list = None):
        """
        Inicia uma sessão de chat, opcionalmente com um histórico de conversas.
        History deve ser uma lista de dicionários: [{'role': 'user'/'model', 'parts': [text]}]
        """
        if history is None:
            history = []
        return self.model.start_chat(history=history)