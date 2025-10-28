from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import lost_items


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lost and Found API",
    description="A simple API for managing lost and found items.",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Lost and Found API"}

