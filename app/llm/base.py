class LLMProvider:
    '''
    Essa classe define a interface que qualquer provedor de LLM (Gemini, OpenAI, etc.) deverá seguir.
    Ela define os métodos que devem ser implementados pelos provedores de LLM.
    '''
    def gerar_resposta(self, mensagem: str, contexto: str = "") -> str:
        raise NotImplementedError