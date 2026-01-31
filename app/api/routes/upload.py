"""
Upload Route - Handle lost/found item submissions
"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database import Item, ItemType
from app.core.security import generate_tracking_token
from app.services.image_processor import process_and_save_image
from datetime import datetime
import os

router = APIRouter()

@router.post("/upload/lost")
async def upload_lost_item(
    item_name: str = Form(...),
    description: str = Form(...),
    contact_info: str = Form(None),
    location: str = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a lost item
    
    Returns tracking token for future queries
    """
    try:
        # Generate tracking token
        tracking_token = generate_tracking_token()
        
        # Process and save image
        image_path = await process_and_save_image(
            image,
            item_type="lost",
            tracking_token=tracking_token
        )
        
        # Create database entry
        new_item = Item(
            tracking_token=tracking_token,
            item_type=ItemType.LOST,
            item_name=item_name.strip().lower(),
            description=description.strip().lower(),
            image_path=image_path,
            contact_info=contact_info,
            location=location
        )
        
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        return {
            "status": "success",
            "message": "Lost item uploaded successfully",
            "tracking_token": tracking_token,
            "item_id": new_item.id,
            "next_steps": "Use this tracking token to check for matches later"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/upload/found")
async def upload_found_item(
    item_name: str = Form(...),
    description: str = Form(...),
    contact_info: str = Form(None),
    location: str = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a found item
    
    Automatically triggers matching against lost items
    """
    try:
        # Generate tracking token
        tracking_token = generate_tracking_token()
        
        # Process and save image
        image_path = await process_and_save_image(
            image,
            item_type="found",
            tracking_token=tracking_token
        )
        
        # Create database entry
        new_item = Item(
            tracking_token=tracking_token,
            item_type=ItemType.FOUND,
            item_name=item_name.strip().lower(),
            description=description.strip().lower(),
            image_path=image_path,
            contact_info=contact_info,
            location=location
        )
        
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        # TODO: Trigger background matching task here
        # from app.services.matcher import trigger_matching
        # trigger_matching(new_item.id, db)
        
        return {
            "status": "success",
            "message": "Found item uploaded successfully",
            "tracking_token": tracking_token,
            "item_id": new_item.id,
            "next_steps": "System will automatically search for matches"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/upload/stats")
async def get_upload_stats(db: Session = Depends(get_db)):
    """Get upload statistics"""
    total_lost = db.query(Item).filter(Item.item_type == ItemType.LOST).count()
    total_found = db.query(Item).filter(Item.item_type == ItemType.FOUND).count()
    
    return {
        "total_lost_items": total_lost,
        "total_found_items": total_found,
        "total_items": total_lost + total_found
    }