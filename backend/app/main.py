from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import documents, extraction, learning

app = FastAPI(
    title="Document Extraction API",
    description="API for extracting data from delivery notes using OCR",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(extraction.router, prefix="/api/extraction", tags=["extraction"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])


@app.get("/")
async def root():
    return {
        "message": "Document Extraction API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
