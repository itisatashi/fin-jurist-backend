from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.message import MessageCreate, Message
from app.models.message import Message as MessageModel
from app.models.chat import Chat as ChatModel
from app.models.user import User as UserModel
from app.core.dependencies import get_current_user
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/", response_model=Message)
async def send_message(
    message: MessageCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify chat belongs to user
    chat = db.query(ChatModel).filter(
        ChatModel.id == message.chat_id,
        ChatModel.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # Save user message
    user_message = MessageModel(
        chat_id=message.chat_id,
        content=message.content,
        role="user"
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # Get chat history for context
    chat_messages = db.query(MessageModel).filter(
        MessageModel.chat_id == message.chat_id
    ).order_by(MessageModel.timestamp.asc()).limit(10).all()
    
    # Format messages for AI
    messages_for_ai = []
    for msg in chat_messages:
        messages_for_ai.append({
            "role": msg.role,
            "content": msg.content
        })
    
    # Add current user message
    messages_for_ai.append({
        "role": "user",
        "content": message.content
    })
    
    # Get AI response using Novita AI
    ai_response = await ai_service.generate_response(messages_for_ai)
    
    # Save AI response
    ai_message = MessageModel(
        chat_id=message.chat_id,
        content=ai_response,
        role="assistant"
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)
    
    return ai_message

@router.get("/{chat_id}", response_model=List[Message])
def get_chat_messages(
    chat_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify chat belongs to user
    chat = db.query(ChatModel).filter(
        ChatModel.id == chat_id,
        ChatModel.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    messages = db.query(MessageModel).filter(
        MessageModel.chat_id == chat_id
    ).order_by(MessageModel.timestamp.asc()).all()
    
    return messages

@router.delete("/{message_id}")
def delete_message(
    message_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get message and verify ownership through chat
    message = db.query(MessageModel).join(ChatModel).filter(
        MessageModel.id == message_id,
        ChatModel.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    db.delete(message)
    db.commit()
    
    return {"message": "Message deleted successfully"}

@router.post("/analyze-contract")
async def analyze_contract(
    contract_data: dict,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze financial contracts for risks and issues
    """
    contract_text = contract_data.get("contract_text", "")
    contract_type = contract_data.get("contract_type", "financial")
    
    if not contract_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contract text is required"
        )
    
    try:
        analysis = await ai_service.analyze_contract(contract_text, contract_type)
        return {
            "success": True,
            "analysis": analysis,
            "contract_type": contract_type
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing contract: {str(e)}"
        )

@router.post("/detect-fraud")
async def detect_fraud(
    fraud_data: dict,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze potential financial fraud or scam
    """
    description = fraud_data.get("description", "")
    
    if not description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description is required"
        )
    
    try:
        fraud_analysis = await ai_service.detect_financial_fraud(description)
        return {
            "success": True,
            "fraud_analysis": fraud_analysis
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing fraud risk: {str(e)}"
        )

@router.post("/generate-template")
async def generate_template(
    template_data: dict,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate legal document templates
    """
    document_type = template_data.get("document_type", "")
    details = template_data.get("details", "")
    
    if not document_type.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document type is required"
        )
    
    try:
        template = await ai_service.generate_document_template(document_type, details)
        return {
            "success": True,
            "template": template,
            "document_type": document_type
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating template: {str(e)}"
        )

@router.post("/financial-education")
async def financial_education(
    education_data: dict,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Provide financial education and explanations
    """
    topic = education_data.get("topic", "")
    
    if not topic.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Topic is required"
        )
    
    try:
        education_content = await ai_service.provide_financial_education(topic)
        return {
            "success": True,
            "education_content": education_content,
            "topic": topic
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error providing education: {str(e)}"
        )