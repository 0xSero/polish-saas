from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Alert, User
from schemas import Alert as AlertSchema, AlertCreate
from api.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[AlertSchema])
async def get_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all alerts for current user"""
    alerts = db.query(Alert).filter(Alert.user_id == current_user.id).all()
    return alerts


@router.post("/", response_model=AlertSchema)
async def create_alert(
    alert: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new air quality alert"""
    # Premium feature check
    if not current_user.is_premium:
        # Free users can only have 1 alert
        existing_alerts = db.query(Alert).filter(Alert.user_id == current_user.id).count()
        if existing_alerts >= 1:
            raise HTTPException(
                status_code=403,
                detail="Free users can only create 1 alert. Upgrade to premium for unlimited alerts."
            )

    db_alert = Alert(**alert.dict(), user_id=current_user.id)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.put("/{alert_id}", response_model=AlertSchema)
async def update_alert(
    alert_id: int,
    alert_update: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing alert"""
    db_alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()

    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    for key, value in alert_update.dict().items():
        setattr(db_alert, key, value)

    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an alert"""
    db_alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()

    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(db_alert)
    db.commit()
    return {"message": "Alert deleted successfully"}


@router.post("/{alert_id}/toggle")
async def toggle_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle alert active status"""
    db_alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()

    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db_alert.is_active = not db_alert.is_active
    db.commit()
    db.refresh(db_alert)
    return db_alert
