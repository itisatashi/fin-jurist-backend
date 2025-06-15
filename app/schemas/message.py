from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class MessageBase(BaseModel):
    content: str
    role: Literal["user", "assistant"]

class MessageCreate(MessageBase):
    chat_id: str

class MessageInDBBase(MessageBase):
    id: str
    chat_id: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class Message(MessageInDBBase):
    pass