"""
Search Route - Find matches using ML model (FIXED VERSION)
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
import os

router = APIRouter()

@router.get("/search/{tracking_token}")
async def search_matches(
    tracking_token: str,
    top_k: int = 5,
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
    print(f"\n{'='*60}")
    print(f"🔍 SEARCH REQUEST for token: {tracking_token}")
    print(f"{'='*60}")
    
    # Find the query item
    query_item = db.query(Item).filter(
        Item.tracking_token == tracking_token
    ).first()
    
    if not query_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    print(f"✅ Query item found:")
    print(f"   ID: {query_item.id}")
    print(f"   Type: {query_item.item_type.value}")
    print(f"   Name: {query_item.item_name}")
    print(f"   Description: {query_item.description}")
    
    # Determine search direction
    if query_item.item_type == ItemType.LOST:
        # Search in found items
        candidate_items = db.query(Item).filter(
            Item.item_type == ItemType.FOUND
        ).all()
        search_type = "FOUND"
        print(f"\n🔎 Searching for FOUND items (Lost item searching)")
    else:
        # Search in lost items
        candidate_items = db.query(Item).filter(
            Item.item_type == ItemType.LOST
        ).all()
        search_type = "LOST"
        print(f"\n🔎 Searching for LOST items (Found item searching)")
    
    print(f"   Total candidates: {len(candidate_items)}")
    
    if not candidate_items:
        return {
            "status": "no_candidates",
            "message": f"No {search_type} items available to match",
            "query_item": {
                "id": query_item.id,
                "token": query_item.tracking_token,
                "type": query_item.item_type.value,
                "name": query_item.item_name,
                "description": query_item.description
            },
            "matches": []
        }
    
    # Load query image
    query_image_full_path = os.path.join("static", query_item.image_path)
    print(f"\n📸 Loading query image from: {query_image_full_path}")
    
    if not os.path.exists(query_image_full_path):
        print(f"❌ Query image not found at: {query_image_full_path}")
        raise HTTPException(status_code=500, detail=f"Query image not found: {query_item.image_path}")
    
    query_img = load_clean_image(query_item.image_path)
    if query_img is None:
        print(f"❌ Failed to load query image")
        raise HTTPException(status_code=500, detail="Failed to load query image")
    
    print(f"✅ Query image loaded successfully")
    
    # Extract features and compute matches
    matches = []
    
    print(f"\n🤖 Starting ML matching process...")
    print(f"{'='*60}")
    
    for idx, candidate in enumerate(candidate_items, 1):
        try:
            print(f"\n[{idx}/{len(candidate_items)}] Processing candidate ID: {candidate.id}")
            print(f"   Name: {candidate.item_name}")
            print(f"   Description: {candidate.description}")
            
            # Load candidate image
            candidate_image_full_path = os.path.join("static", candidate.image_path)
            print(f"   Image path: {candidate_image_full_path}")
            
            if not os.path.exists(candidate_image_full_path):
                print(f"   ⚠️ Candidate image not found, skipping...")
                continue
            
            candidate_img = load_clean_image(candidate.image_path)
            if candidate_img is None:
                print(f"   ⚠️ Failed to load candidate image, skipping...")
                continue
            
            print(f"   ✅ Candidate image loaded")
            
            # Extract all features
            print(f"   🔧 Extracting features...")
            features = feature_extractor.extract_all_features(
                img1=query_img,
                img2=candidate_img,
                text1=query_item.description,
                text2=candidate.description,
                item_name=query_item.item_name
            )
            
            print(f"   📊 Features extracted:")
            print(f"      DINOv2: {features[0]:.4f}")
            print(f"      SIFT: {features[1]:.4f}")
            print(f"      Text: {features[2]:.4f}")
            print(f"      Name: {features[3]:.4f}")
            print(f"      Color: {features[4]:.4f}")
            
            # Get ML prediction
            prediction, confidence = ml_service.predict(features)
            
            print(f"   🎯 ML Prediction:")
            print(f"      Confidence: {confidence:.4f} ({confidence*100:.2f}%)")
            print(f"      Is Match: {'YES ✅' if prediction == 1 else 'NO ❌'}")
            
            # Store match result in database
            if query_item.item_type == ItemType.LOST:
                lost_id = query_item.id
                found_id = candidate.id
            else:
                lost_id = candidate.id
                found_id = query_item.id
            
            match_record = Match(
                lost_item_id=lost_id,
                found_item_id=found_id,
                overall_score=float(confidence),
                dino_similarity=float(features[0]),
                sift_similarity=float(features[1]),
                text_similarity=float(features[2]),
                item_name_similarity=float(features[3]),
                color_match=float(features[4]),
                is_match=int(prediction),
                confidence=float(confidence * 100)
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
            print(f"   ❌ Error processing candidate {candidate.id}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    # Commit match records
    try:
        db.commit()
        print(f"\n✅ Match records saved to database")
    except Exception as e:
        print(f"⚠️ Failed to save match records: {e}")
        db.rollback()
    
    # Sort by confidence and get top K
    matches.sort(key=lambda x: x['confidence'], reverse=True)
    top_matches = matches[:top_k]
    
    print(f"\n{'='*60}")
    print(f"📊 SEARCH RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Total candidates checked: {len(candidate_items)}")
    print(f"Total matches found: {len([m for m in matches if m['is_match']])}")
    print(f"Top {min(top_k, len(matches))} matches returned")
    print(f"{'='*60}\n")
    
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
        
        if lost_item and found_item:
            results.append({
                "match_id": match.id,
                "confidence": round(match.confidence, 2),
                "lost_item": {
                    "name": lost_item.item_name,
                    "description": lost_item.description,
                    "token": lost_item.tracking_token
                },
                "found_item": {
                    "name": found_item.item_name,
                    "description": found_item.description,
                    "token": found_item.tracking_token
                },
                "matched_at": match.created_at.isoformat() if match.created_at else None
            })
    
    return {
        "status": "success",
        "recent_matches": results
    }