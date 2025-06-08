from app.agents.models.gemini import GeminiModel
from app.agents.tools.notion_tools import available_tools

class ChatAgent:
    """
    Gerencia a lógica de conversação, incluindo o acionamento de ferramentas.
    """

    def __init__(self, history: list = None):
        self.model_wrapper = GeminiModel()
        self.chat = self.model_wrapper.start_chat(history=history)

    async def get_response(self, prompt: str) -> str:
        """
        Processa um prompt, aciona ferramentas se necessário e retorna a resposta final.
        """
        response = self.chat.send_message(prompt)
        
        # O SDK do Google Generative AI processa automaticamente as function calls
        # Só precisamos retornar o texto final
        try:
            return response.text
        except ValueError as e:
            if "function_call" in str(e):
                print(f"🚀 Function call detectado mas não processado automaticamente")
                # Para versões mais antigas do SDK, processar manualmente
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call') and part.function_call:
                                function_call = part.function_call
                                tool_name = function_call.name
                                tool_args = dict(function_call.args) if function_call.args else {}
                                
                                print(f"🔧 Executando manualmente: {tool_name}({tool_args})")
                                
                                # Buscar e executar a ferramenta
                                for tool in available_tools:
                                    if tool.__name__ == tool_name:
                                        result = tool(**tool_args)
                                        return f"Resultado da ferramenta {tool_name}:\n\n{result}"
                                
                                return f"Ferramenta {tool_name} chamada mas não encontrada"
                
                return "Function call detectado mas não consegui processar"
            else:
                return f"Erro ao obter resposta: {e}"