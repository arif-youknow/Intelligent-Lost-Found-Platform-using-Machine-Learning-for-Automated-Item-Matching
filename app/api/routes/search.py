"""
Search Route - Find matches using ML model
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database_models import Item, Match, ItemType
from app.services.ml_service import ml_service
from app.services.feature_extractor import feature_extractor
from app.services.image_processor import load_clean_image
from typing import List, Dict
import numpy as np

router = APIRouter()

@router.get("/search/{tracking_token}")
async def search_matches(
    tracking_token: str,
    top_k: int = 2,
    db: Session = Depends(get_db)
):
    """
    Search for matching items using tracking token
    
    Args:
        tracking_token: The token received when uploading an item
        top_k: Number of top matches to return (default: 5)
    
    Returns:
        List of potential matches with confidence scores
    """
    # Find the query item
    query_item = db.query(Item).filter(
        Item.tracking_token == tracking_token
    ).first()
    
    if not query_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Determine search direction
    if query_item.item_type == ItemType.LOST:
        # Search in found items
        candidate_items = db.query(Item).filter(
            Item.item_type == ItemType.FOUND
        ).all()
        search_type = "found"
    else:
        # Search in lost items
        candidate_items = db.query(Item).filter(
            Item.item_type == ItemType.LOST
        ).all()
        search_type = "lost"
    
    if not candidate_items:
        return {
            "status": "no_candidates",
            "message": f"No {search_type} items available to match",
            "matches": []
        }
    
    # Load query image
    query_img = load_clean_image(query_item.image_path)
    if query_img is None:
        raise HTTPException(status_code=500, detail="Failed to load query image")
    
    # Extract features and compute matches
    matches = []
    
    for candidate in candidate_items:
        try:
            # Load candidate image
            candidate_img = load_clean_image(candidate.image_path)
            if candidate_img is None:
                continue
            
            # Extract all features
            features = feature_extractor.extract_all_features(
                img1=query_img,
                img2=candidate_img,
                text1=query_item.description,
                text2=candidate.description,
                item_name=query_item.item_name
            )
            
            # Get ML prediction
            prediction, confidence = ml_service.predict(features)
            
            # Store match result
            match_record = Match(
                lost_item_id=query_item.id if query_item.item_type == ItemType.LOST else candidate.id,
                found_item_id=candidate.id if query_item.item_type == ItemType.LOST else query_item.id,
                overall_score=confidence,
                dino_similarity=float(features[0]),
                sift_similarity=float(features[1]),
                text_similarity=float(features[2]),
                item_name_similarity=float(features[3]),
                color_match=float(features[4]),
                is_match=prediction,
                confidence=confidence
            )
            
            db.add(match_record)
            
            # Add to results
            matches.append({
                "candidate_id": candidate.id,
                "candidate_token": candidate.tracking_token,
                "item_name": candidate.item_name,
                "description": candidate.description,
                "image_url": f"/static/{candidate.image_path}",
                "contact_info": candidate.contact_info,
                "location": candidate.location,
                "is_match": bool(prediction),
                "confidence": round(confidence * 100, 2),
                "similarity_breakdown": {
                    "visual_similarity": round(float(features[0]) * 100, 2),
                    "texture_similarity": round(float(features[1]) * 100, 2),
                    "description_similarity": round(float(features[2]) * 100, 2),
                    "name_similarity": round(float(features[3]) * 100, 2),
                    "color_match": "Yes" if features[4] > 0.7 else "No"
                }
            })
        
        except Exception as e:
            print(f"⚠️ Error processing candidate {candidate.id}: {e}")
            continue
    
    # Commit match records
    db.commit()
    
    # Sort by confidence and get top K
    matches.sort(key=lambda x: x['confidence'], reverse=True)
    top_matches = matches[:top_k]
    
    return {
        "status": "success",
        "query_item": {
            "id": query_item.id,
            "token": query_item.tracking_token,
            "type": query_item.item_type.value,
            "name": query_item.item_name,
            "description": query_item.description
        },
        "total_candidates_checked": len(candidate_items),
        "total_matches_found": len([m for m in matches if m['is_match']]),
        "top_matches": top_matches
    }


@router.get("/search/recent-matches")
async def get_recent_matches(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent successful matches"""
    recent = db.query(Match).filter(
        Match.is_match == 1
    ).order_by(
        Match.created_at.desc()
    ).limit(limit).all()
    
    results = []
    for match in recent:
        lost_item = db.query(Item).get(match.lost_item_id)
        found_item = db.query(Item).get(match.found_item_id)
        
        results.append({
            "match_id": match.id,
            "confidence": round(match.confidence * 100, 2),
            "lost_item": {
                "name": lost_item.item_name,
                "description": lost_item.description
            },
            "found_item": {
                "name": found_item.item_name,
                "description": found_item.description
            },
            "matched_at": match.created_at.isoformat()
        })
    
    return {
        "status": "success",
        "recent_matches": results
    }