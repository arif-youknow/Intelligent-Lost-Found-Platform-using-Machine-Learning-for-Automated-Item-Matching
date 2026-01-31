import os
from anyio import Path
from dotenv import load_dotenv


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Lost and Found AI"
    PROJECT_VERSION: str = "1.0.0"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Paths
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./static/uploads")
    MODEL_DIR: str = os.getenv("MODEL_DIR", "./ml_models")
    
    # Device setup
    DEVICE: str = os.getenv("DEVICE", "cpu")

settings = Settings()