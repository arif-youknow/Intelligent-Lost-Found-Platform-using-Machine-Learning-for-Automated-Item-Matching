"""
Upload Route - Handle lost/found item submissions
"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database_models import Item, ItemType
from app.core.security import generate_tracking_token
from app.services.image_processor import process_and_save_image
from datetime import datetime
import os

router = APIRouter()


#helpar FUNCTION for upload new item

async def handle_item_upload(
        
    item_type: ItemType,
    item_name: str,
    description: str,
    contact_info: str,
    image: UploadFile,
    db: Session

):
    try:
        tracking_token = generate_tracking_token()
        image_path = await process_and_save_image(
            image,
            item_type=item_type.value,
            tracking_token=tracking_token
        )
        new_item = Item(
            tracking_token=tracking_token,
            item_type=item_type,
            item_name=item_name.strip().lower(),
            description=description.strip().lower(),
            image_path=image_path,
            contact_info=contact_info,
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item, tracking_token
    except Exception as e:
        db.rollback()
        raise e







#POST api call


@router.post("/upload/lost")
async def upload_lost_item(
    item_name: str = Form(...),
    description: str = Form(...),
    contact_info: str = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a lost item
    
    Returns tracking token for future queries
    """
    try:
        item, token = await handle_item_upload(ItemType.LOST, item_name, description, contact_info, image, db)
        return {
            "status": "success",
            "tracking_token": token,
            "item_id": item.id,
            "message": "Lost item uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/upload/found")
async def upload_found_item(
    item_name: str = Form(...),
    description: str = Form(...),
    contact_info: str = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a found item
    
    Automatically triggers matching against lost items
    """
    try:
        item, token = await handle_item_upload(ItemType.FOUND, item_name, description, contact_info, image, db)
        
        
        return {
            "status": "success",
            "tracking_token": token,
            "item_id": item.id,
            "message": "Found item uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
