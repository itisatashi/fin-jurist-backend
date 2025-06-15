from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.chat import ChatCreate, Chat, ChatUpdate
from app.models.chat import Chat as ChatModel
from app.models.user import User as UserModel
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=Chat)
def create_chat(
    chat: ChatCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_chat = ChatModel(
        title=chat.title,
        user_id=current_user.id
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@router.get("/", response_model=List[Chat])
def get_user_chats(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chats = db.query(ChatModel).filter(ChatModel.user_id == current_user.id).order_by(ChatModel.created_at.desc()).all()
    return chats

@router.get("/{chat_id}", response_model=Chat)
def get_chat(
    chat_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(ChatModel).filter(
        ChatModel.id == chat_id,
        ChatModel.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    return chat

@router.put("/{chat_id}", response_model=Chat)
def update_chat(
    chat_id: str,
    chat_update: ChatUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(ChatModel).filter(
        ChatModel.id == chat_id,
        ChatModel.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    if chat_update.title is not None:
        chat.title = chat_update.title
    
    db.commit()
    db.refresh(chat)
    return chat

@router.delete("/{chat_id}")
def delete_chat(
    chat_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(ChatModel).filter(
        ChatModel.id == chat_id,
        ChatModel.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    db.delete(chat)
    db.commit()
    
    return {"message": "Chat deleted successfully"}