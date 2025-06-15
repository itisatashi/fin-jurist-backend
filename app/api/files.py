from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from pathlib import Path
import PyPDF2
from docx import Document
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import io

from app.database import get_db
from app.models.user import User as UserModel
from app.core.dependencies import get_current_user
from app.services.ai_service import ai_service

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process files (PDF, Word, Audio)"""
    
    # Check file size (max 10MB)
    if file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size too large. Maximum 10MB allowed."
        )
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOADS_DIR / unique_filename
    
    try:
        # Save file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Process file based on type
        processed_content = ""
        file_type = ""
        
        if file_extension == ".pdf":
            processed_content = extract_pdf_text(file_path)
            file_type = "PDF Document"
        elif file_extension in [".doc", ".docx"]:
            processed_content = extract_word_text(file_path)
            file_type = "Word Document"
        elif file_extension in [".wav", ".mp3", ".m4a", ".ogg"]:
            processed_content = transcribe_audio(file_path)
            file_type = "Audio Recording"
        elif file_extension in [".jpg", ".jpeg", ".png", ".gif"]:
            processed_content = "Image uploaded successfully. Please describe what you'd like me to analyze about this image."
            file_type = "Image"
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type. Supported: PDF, Word, Audio (WAV, MP3), Images"
            )
        
        # Generate AI analysis if content was extracted
        ai_analysis = ""
        if processed_content and file_type in ["PDF Document", "Word Document"]:
            ai_analysis = await analyze_document_with_ai(processed_content, file_type)
        elif file_type == "Audio Recording":
            ai_analysis = await analyze_audio_content_with_ai(processed_content)
        
        # Clean up file after processing
        os.remove(file_path)
        
        return {
            "success": True,
            "data": {
                "filename": file.filename,
                "file_type": file_type,
                "content": processed_content,
                "ai_analysis": ai_analysis,
                "size": file.size
            }
        }
        
    except Exception as e:
        # Clean up file if error occurs
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )

def extract_pdf_text(file_path: Path) -> str:
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error reading PDF: {str(e)}"
        )

def extract_word_text(file_path: Path) -> str:
    """Extract text from Word document"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error reading Word document: {str(e)}"
        )

def transcribe_audio(file_path: Path) -> str:
    """Transcribe audio to text"""
    try:
        # Convert audio to WAV format if needed
        audio = AudioSegment.from_file(file_path)
        
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            audio.export(temp_wav.name, format="wav")
            
            # Transcribe audio
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_wav.name) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='uz-UZ')
            
            # Clean up temporary file
            os.unlink(temp_wav.name)
            
            return text
    except sr.UnknownValueError:
        return "Audio was not clear enough to transcribe. Please try recording again."
    except sr.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Speech recognition service error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error transcribing audio: {str(e)}"
        )

async def analyze_document_with_ai(content: str, file_type: str) -> str:
    """Analyze document content with AI"""
    try:
        prompt = f"""
You are a legal and financial expert. Analyze the following {file_type} content and provide:

1. **Document Summary**: Brief overview of the document
2. **Key Points**: Main legal and financial points
3. **Potential Risks**: Any legal or financial risks identified
4. **Recommendations**: Suggested actions or considerations
5. **Important Clauses**: Critical terms and conditions to note

Document Content:
{content[:4000]}  # Limit content to avoid token limits

Provide your analysis in a clear, structured format.
"""
        
        messages = [{"role": "user", "content": prompt}]
        analysis = await ai_service.generate_response(messages)
        return analysis
        
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"

async def analyze_audio_content_with_ai(transcribed_text: str) -> str:
    """Analyze transcribed audio content with AI"""
    try:
        prompt = f"""
You are a legal and financial expert. The user has sent a voice message that was transcribed to:

"{transcribed_text}"

Provide a helpful response addressing their legal or financial question or concern. If the transcription seems unclear, ask for clarification.
"""
        
        messages = [{"role": "user", "content": prompt}]
        analysis = await ai_service.generate_response(messages)
        return analysis
        
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"

@router.post("/text-to-speech")
async def text_to_speech(
    text: str,
    current_user: UserModel = Depends(get_current_user)
):
    """Convert text to speech (placeholder for future implementation)"""
    # This would integrate with a TTS service like Google Cloud TTS or Azure Speech
    return {
        "success": True,
        "message": "Text-to-speech feature will be implemented with cloud TTS service",
        "text": text
    }