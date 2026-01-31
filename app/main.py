import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import search, tracking, upload


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/uploads/lost", exist_ok=True)
os.makedirs("static/uploads/found", exist_ok=True)
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