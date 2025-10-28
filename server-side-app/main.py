from fastapi import FastAPI
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import found_items, lost_items
from fastapi.staticfiles import StaticFiles


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lost and Found API",
    description="A simple API for managing lost and found items.",
    version="1.0.0",
)


origins = [
    "http://localhost",
    "http://localhost:5173",  
    "http://127.0.0.1:5173"  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(found_items.router, prefix="/api")
app.include_router(lost_items.router, prefix="/api")

app.mount("/uploads/found", StaticFiles(directory="uploads/found"), name="found_uploads")
app.mount("/uploads/lost", StaticFiles(directory="uploads/lost"), name="lost_uploads")




