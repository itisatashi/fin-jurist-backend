# Fin-Jurist Backend API

## 📋 About the Project

Fin-Jurist is the backend part of a financial-legal consultation system. This API is built using the FastAPI framework and provides AI-powered legal consultation services.

## 🏗️ Architecture

### Technologies
- **FastAPI** - Modern, fast, and high-performance web framework
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Authentication
- **OpenAI API** - AI responses
- **PyPDF2, python-docx** - File processing
- **SpeechRecognition** - Audio to text conversion

### Project Structure
```
fin-jurist-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and configuration
│   ├── database.py          # Database connection
│   ├── api/                 # API endpoints
│   │   ├── auth.py          # Authentication
│   │   ├── chats.py         # Chat management
│   │   ├── messages.py      # Message management
│   │   └── files.py         # File upload and processing
│   ├── core/                # Core configurations
│   │   ├── config.py        # Application settings
│   │   ├── security.py      # Security functions
│   │   └── dependencies.py  # Common dependencies
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py          # User model
│   │   ├── chat.py          # Chat model
│   │   └── message.py       # Message model
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py          # User schemas
│   │   ├── chat.py          # Chat schemas
│   │   └── message.py       # Message schemas
│   └── services/            # Business logic
│       └── ai_service.py    # AI services
├── alembic/                 # Database migrations
├── uploads/                 # Uploaded files
├── requirements.txt         # Python libraries
├── alembic.ini             # Alembic configuration
├── .env                    # Environment variables
└── fin_jurist.db           # SQLite database
```

## 🚀 Installation and Setup

### 1. Requirements
- Python 3.8+
- pip (Python package manager)

### 2. Clone the Project
```bash
cd fin-jurist-backend
```

### 3. Create Virtual Environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate  # For Windows
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file and add the following variables:
```env
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=sqlite:///./fin_jurist.db
ALLOWED_ORIGINS=http://localhost:3000
```

### 6. Create Database
```bash
alembic upgrade head
```

### 7. Start the Server
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Current user information

### Chats
- `GET /chats/` - Get all chats
- `POST /chats/` - Create new chat
- `GET /chats/{chat_id}` - Get specific chat
- `PUT /chats/{chat_id}` - Update chat
- `DELETE /chats/{chat_id}` - Delete chat

### Messages
- `GET /messages/{chat_id}` - Get chat messages
- `POST /messages/` - Send new message
- `DELETE /messages/{message_id}` - Delete message

### Files
- `POST /files/upload` - Upload and process file
- `POST /files/text-to-speech` - Convert text to speech

## 🔧 Features

### AI Integration
- Integration with OpenAI GPT model
- Financial-legal consultation services
- Contextual responses
- File analysis (PDF, Word, Audio)

### Security
- JWT token authentication
- Password hashing (bcrypt)
- CORS configuration
- Data validation

### File Processing
- PDF text extraction
- Word document reading
- Audio to text conversion
- File size limit (10MB)

## 🧪 Testing

### View API Documentation
After starting the server, go to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Health check
```bash
curl http://localhost:8000/health
```

## 🔄 Database Migrations

### Create New Migration
```bash
alembic revision --autogenerate -m "migration description"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migrations
```bash
alembic downgrade -1
```

## 📝 Development

### Code Formatting
```bash
pip install black
black .
```

### Linting
```bash
pip install flake8
flake8 .
```

## 🐛 Troubleshooting

### Common Issues
1. **Port busy** - Use different port: `--port 8001`
2. **Database error** - Re-run migrations
3. **OpenAI API error** - Check API key
4. **CORS error** - Check `ALLOWED_ORIGINS`

### View Logs
When the server starts, all logs are displayed in the console.

## 📞 Help

If issues arise:
1. Check that all libraries in requirements.txt are installed
2. Verify .env file is properly configured
3. Ensure Python version is 3.8+
4. Confirm database migrations have been applied

---

**Note:** This project is in development mode. Additional security configurations will be needed for production.