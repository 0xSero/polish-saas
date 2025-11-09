from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import get_db
from models import User
from api.auth import get_current_user

router = APIRouter()


@router.post("/subscribe")
async def subscribe_premium(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Subscribe to premium plan
    In production, integrate with payment gateway (Stripe, PayU, etc.)
    """
    if current_user.is_premium:
        raise HTTPException(status_code=400, detail="Already subscribed to premium")

    # In production, verify payment here
    # For now, just enable premium
    current_user.is_premium = True
    db.commit()

    return {
        "message": "Successfully subscribed to premium",
        "premium_until": datetime.utcnow() + timedelta(days=30)
    }


@router.post("/unsubscribe")
async def unsubscribe_premium(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel premium subscription"""
    if not current_user.is_premium:
        raise HTTPException(status_code=400, detail="Not subscribed to premium")

    current_user.is_premium = False
    db.commit()

    return {"message": "Successfully unsubscribed from premium"}


@router.get("/status")
async def get_subscription_status(current_user: User = Depends(get_current_user)):
    """Get current subscription status"""
    return {
        "is_premium": current_user.is_premium,
        "email": current_user.email,
        "features": {
            "unlimited_alerts": current_user.is_premium,
            "faster_updates": current_user.is_premium,
            "historical_data": current_user.is_premium,
            "advanced_forecasts": current_user.is_premium,
        }
    }
