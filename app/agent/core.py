from app.llm.google_provider import GoogleProvider
from app.agent.memory import salvar_historico, recuperar_contexto

llm = GoogleProvider()

def processar_mensagem(mensagem: str, cliente_id: int) -> str:
    contexto = recuperar_contexto(cliente_id)
    resposta = llm.gerar_resposta(mensagem, contexto)
    salvar_historico(cliente_id, mensagem, resposta)
    return resposta