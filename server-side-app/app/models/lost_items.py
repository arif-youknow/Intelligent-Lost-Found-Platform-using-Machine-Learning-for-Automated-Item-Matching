from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from app.core.database import Base
import datetime

class LostItem(Base):
    __tablename__ = "lost_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    date_posted = Column(DateTime, default=datetime.datetime.now)
    item_type = Column(Enum('lost', 'resolved'), nullable=False, default='lost')
    image_url = Column(String(512), nullable=False)
    