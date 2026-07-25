from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.dashboard import router as dashboard_router
from routes.job import router as job_router
from routes.health import router as health_router
from routes.upload import router as upload_router
from routes.ranking import router as ranking_router
from routes.chat import router as chat_router
from routes.pdf import router as pdf_router
from routes.ats import router as ats_router
from database.db import Base
from database.db import engine

import models.resume
import models.job

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Hiring Assistant",
    version="1.0.0",
    description="AI Resume Screening System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(health_router)
app.include_router(upload_router)
app.include_router(job_router)
app.include_router(pdf_router)
app.include_router(ranking_router)
app.include_router(chat_router)
# app.include_router(ats_router)

@app.get("/")
def root():
    return {
        "message": "🚀 AI Hiring Assistant Backend Running"
    }