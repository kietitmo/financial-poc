from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.pdf_router import router as pdf_router

app = FastAPI(title="BCTC Processing API (SOLID + Celery + Logger)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(pdf_router, prefix="/api/pdf", tags=["pdf"])
