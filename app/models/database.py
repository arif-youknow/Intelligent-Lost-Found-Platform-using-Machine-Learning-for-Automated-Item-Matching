from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ItemType(enum.Enum):
    LOST = "lost"
    FOUND = "found"

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    tracking_token = Column(String(50), unique=True, index=True)
    item_type = Column(Enum(ItemType), nullable=False)
    item_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    image_path = Column(String(500), nullable=False)
    contact_info = Column(String(200))
    location = Column(String(200))
    dino_feature = Column(Text)
    sift_keypoints = Column(Integer)
    text_embedding = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True)
    lost_item_id = Column(Integer, index=True)
    found_item_id = Column(Integer, index=True)
    overall_score = Column(Float)
    dino_similarity = Column(Float)
    sift_similarity = Column(Float)
    text_similarity = Column(Float)
    item_name_similarity = Column(Float)
    color_match = Column(Float)
    is_match = Column(Integer)
    confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())