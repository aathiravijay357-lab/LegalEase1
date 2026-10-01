from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router

app = FastAPI(
    title="LegalEase API",
    version="1.0.0",
    description="Backend API for the LegalEase AI-assisted document drafting application.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "application": "LegalEase",
        "status": "running",
        "message": "LegalEase backend is running.",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
