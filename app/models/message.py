from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    chat_id = Column(String, ForeignKey("chats.id"), nullable=False)
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    chat = relationship("Chat", back_populates="messages")