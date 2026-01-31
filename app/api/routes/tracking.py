"""
Tracking Route - Track items using tracking token
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database import Item
from app.core.security import validate_tracking_token

router = APIRouter()

@router.get("/track/{tracking_token}")
async def track_item(
    tracking_token: str,
    db: Session = Depends(get_db)
):
    """
    Get item details using tracking token
    
    Args:
        tracking_token: The token received during upload
    
    Returns:
        Item details and status
    """
    # Validate token format
    if not validate_tracking_token(tracking_token):
        raise HTTPException(
            status_code=400,
            detail="Invalid tracking token format"
        )
    
    # Find item
    item = db.query(Item).filter(
        Item.tracking_token == tracking_token
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found with this tracking token"
        )
    
    return {
        "status": "success",
        "item": {
            "id": item.id,
            "tracking_token": item.tracking_token,
            "type": item.item_type.value,
            "name": item.item_name,
            "description": item.description,
            "image_url": f"/static/{item.image_path}",
            "contact_info": item.contact_info,
            "uploaded_at": item.created_at.isoformat() if item.created_at else None
        },
        "message": f"This is a {item.item_type.value} item. Use /api/v1/search/{tracking_token} to find matches."
    }