from datetime import datetime
from app.db.database import SessionLocal
from app.db.models import Mensagem

def salvar_historico(cliente_id: int, pergunta: str, resposta: str):
    db = SessionLocal()
    msg = Mensagem(
        cliente_id=cliente_id,
        pergunta=pergunta,
        resposta=resposta,
        timestamp=datetime.now()
    )
    db.add(msg)
    db.commit()
    db.close()

def recuperar_contexto(cliente_id: int) -> str:
    db = SessionLocal()
    mensagens = db.query(Mensagem).filter_by(cliente_id=cliente_id).order_by(Mensagem.timestamp.desc()).limit(5).all()
    contexto = "\n".join([f"Q: {m.pergunta}\nA: {m.resposta}" for m in reversed(mensagens)])
    db.close()
    return contexto