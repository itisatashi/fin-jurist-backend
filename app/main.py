from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.database import create_tables
from app.api import auth, chats, messages, files

# Create tables on startup
create_tables()

app = FastAPI(
    title="Fin-Jurist API",
    description="Legal-Financial Consultation System API",
    version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chats.router, prefix="/chats", tags=["Chats"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(files.router, prefix="/files", tags=["Files"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Fin-Jurist API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )