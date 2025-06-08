from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class Mensagem(Base):
    __tablename__ = "mensagens"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, index=True)
    pergunta = Column(String)
    resposta = Column(String)
    timestamp = Column(DateTime)
