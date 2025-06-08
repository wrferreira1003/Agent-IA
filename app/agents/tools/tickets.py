from datetime import datetime

def resumo_tickets(cliente_id: int) -> str:
     # Esta é uma função mockada; depois consultar o banco de dados ou APIs de ticket
    return (
        f"Olá! Hoje é {datetime.now().strftime('%d/%m/%Y')} e você possui 2 tickets abertos, "
        f"1 pendente de resposta e 1 resolvido ontem. \nSe precisar de ajuda, é só me chamar!"
    )