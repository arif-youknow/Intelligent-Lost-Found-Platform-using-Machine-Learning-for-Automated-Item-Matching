import os
from app.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import search, tracking, upload

from app.core.database import engine, Base 



Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Lost & Found System API",
    description="AI-powered Lost & Found matching system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_LOST = os.path.join(settings.UPLOAD_DIR, "lost")
UPLOAD_FOUND = os.path.join(settings.UPLOAD_DIR, "found")


os.makedirs(UPLOAD_LOST, exist_ok=True)
os.makedirs(UPLOAD_FOUND, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")



# Include routers
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(tracking.router, prefix="/api/v1", tags=["Tracking"])



@app.get("/")
async def root():
    return {
        "message": "Lost & Found System API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}