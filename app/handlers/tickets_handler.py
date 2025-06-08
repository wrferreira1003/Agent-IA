
async def obter_resumo_com_personagem(cliente_id: int) -> dict:
    return {
        "cliente_id": cliente_id,
        "personagem": "Capitão IA",
        "mensagem": f"Resumo dos tickets para cliente {cliente_id}",
        "tipo": "resumo_inicial"
    }
