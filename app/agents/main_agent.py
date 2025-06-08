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
        print(f"🤖 Enviando prompt para Gemini: {prompt}")
        response = self.chat.send_message(prompt)
        print(f"🔍 Tipo de resposta: {type(response)}")
        print(f"🔍 Candidatos: {len(response.candidates) if hasattr(response, 'candidates') else 'N/A'}")
        
        # Verificar se há function calls primeiro, antes de tentar obter texto
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and candidate.content:
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call = part.function_call
                        tool_name = function_call.name
                        tool_args = dict(function_call.args) if function_call.args else {}
                        
                        print(f"🔧 Executando ferramenta: {tool_name}({tool_args})")
                        
                        # Buscar e executar a ferramenta
                        for tool in available_tools:
                            if tool.__name__ == tool_name:
                                result = tool(**tool_args)
                                
                                # Enviar resultado de volta para o modelo para formatação
                                function_result = {
                                    "function_call": function_call,
                                    "function_response": {"name": tool_name, "response": result}
                                }
                                
                                # Continuar a conversa com o resultado da função
                                follow_up_response = self.chat.send_message(
                                    [{"function_response": {"name": tool_name, "response": result}}]
                                )
                                
                                return follow_up_response.text
                        
                        return f"Ferramenta {tool_name} não encontrada"
        
        # Se não há function calls, tentar obter texto diretamente
        try:
            print(f"📝 Tentando obter texto da resposta...")
            text = response.text
            print(f"✅ Texto obtido com sucesso: {text[:100]}...")
            return text
        except ValueError as e:
            return f"Erro ao obter resposta: {e}"