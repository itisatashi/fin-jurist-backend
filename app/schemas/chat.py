from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.message import Message

class ChatBase(BaseModel):
    title: str

class ChatCreate(ChatBase):
    pass

class ChatUpdate(BaseModel):
    title: Optional[str] = None

class ChatInDBBase(ChatBase):
    id: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Chat(ChatInDBBase):
    pass

class ChatWithMessages(ChatInDBBase):
    messages: List[Message] = []