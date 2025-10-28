from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from app.core.database import Base
import datetime

class LostItem(Base):
    __tablename__ = "lost_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), nullable=False)
    lost_date = Column(DateTime, default=datetime.datetime.now)
    description = Column(Text, nullable=False)
    item_image = Column(String(512), nullable=False)
    item_status = Column(Enum('lost', 'resolved'), nullable=False, default='lost')

    