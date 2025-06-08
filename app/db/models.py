import uuid
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ChatHistory(Base):
    """
    Modelo SQLAlchemy para armazenar o histórico de mensagens do chat.
    """
    __tablename__ = "chat_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String, nullable=False, index=True) # Para agrupar mensagens de uma mesma conversa
    role = Column(String, nullable=False)  # 'user' ou 'model'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ChatHistory(session_id='{self.session_id}', role='{self.role}')>"
