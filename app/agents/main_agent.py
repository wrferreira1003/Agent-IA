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

        #verificar se o modelo chamou uma ferramenta
        if response.function_calls:
            #Por enquanto vamos lidar apenas com uma chamada de ferramenta por vez
            function_call = response.function_calls[0]
            tool_name = function_call.function.name
            tool_args = function_call.function.arguments

            if tool_name in available_tools:
                tool_func = available_tools[tool_name]

                #Executa a ferramenta e obtém o resultado
                tool_result = tool_func(**tool_args)

                # Envia o resultado da ferramenta de volta para o modelo
                response = self.chat.send_message(
                    [{"function_response": {
                        "name": tool_name,
                        "response": {"result": tool_result}
                    }}]
                )
        return response.text