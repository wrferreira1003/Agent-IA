import google.generativeai as genai
from app.core.config import settings
from app.agents.tools.notion_tools import create_notion_page, search_notion_pages

# Configura a API Key do Google
genai.configure(api_key=settings.GOOGLE_API_KEY)

class GeminiModel:
    """
    Wrapper para o modelo generativo do Google (Gemini).
    """
    def __init__(self, model_name: str = settings.GEMINI_MODEL_NAME):
        # Definir ferramentas diretamente como funções
        self.tools = [create_notion_page, search_notion_pages]
        print(f"🔧 Ferramentas registradas no Gemini: {len(self.tools)}")
        for tool in self.tools:
            print(f"  - {tool.__name__}: {tool.__doc__}")
        
        # Configurar para forçar o uso de ferramentas quando apropriado
        generation_config = genai.GenerationConfig(
            temperature=0.1,
        )
        
        # Configurar modo de uso das ferramentas
        tool_config = genai.ToolConfig(
            function_calling_config=genai.FunctionCallingConfig(
                mode=genai.FunctionCallingConfig.Mode.AUTO,
            )
        )
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=self.tools,
            generation_config=generation_config,
            tool_config=tool_config,
            system_instruction="""Você é o Capitão IA, um assistente que está conectado ao Notion via API.

FERRAMENTAS REAIS DISPONÍVEIS:
- search_notion_pages(): Busca informações REAIS nos documentos do Notion
- create_notion_page(): Cria páginas REAIS no Notion

REGRAS OBRIGATÓRIAS:
1. Quando perguntarem sobre documentos/projetos, use search_notion_pages()
2. As ferramentas são REAIS e funcionais, não simulações
3. SEMPRE use as ferramentas quando apropriado
4. NUNCA diga que as ferramentas são simulações ou não funcionam

Você tem acesso a documentos reais sobre "REST API's com Django Ninja"."""
        )

    def start_chat(self, history: list = None):
        """
        Inicia uma sessão de chat, opcionalmente com um histórico de conversas.
        History deve ser uma lista de dicionários: [{'role': 'user'/'model', 'parts': [text]}]
        """
        if history is None:
            history = []
        return self.model.start_chat(history=history)