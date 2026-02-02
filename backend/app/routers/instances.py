"""
Instance management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/instances", tags=["Instances"])


@router.get("/", response_model=List[schemas.Instance])
async def list_instances(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all instances"""
    if current_user.is_admin:
        instances = db.query(models.Instance).offset(skip).limit(limit).all()
    else:
        instances = db.query(models.Instance).filter(
            models.Instance.owner_id == current_user.id
        ).offset(skip).limit(limit).all()
    
    return instances


@router.get("/{instance_id}", response_model=schemas.Instance)
async def get_instance(
    instance_id: str,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get instance by ID"""
    instance = db.query(models.Instance).filter(models.Instance.id == instance_id).first()
    
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Check permissions
    if not current_user.is_admin and instance.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return instance


@router.post("/", response_model=schemas.Instance, status_code=status.HTTP_201_CREATED)
async def add_instance(
    instance: schemas.InstanceCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a new instance"""
    # Check if instance already exists
    existing = db.query(models.Instance).filter(
        models.Instance.instance_id == instance.instance_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instance ID already exists"
        )
    
    # Create new instance
    db_instance = models.Instance(
        **instance.dict(),
        owner_id=current_user.id,
        status="active"
    )
    
    db.add(db_instance)
    db.commit()
    db.refresh(db_instance)
    
    return db_instance


@router.put("/{instance_id}", response_model=schemas.Instance)
async def update_instance(
    instance_id: str,  # <-- changed from int to str
    instance_update: schemas.InstanceUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an instance"""
    instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
    
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Check permissions
    if not current_user.is_admin and instance.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    update_data = instance_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(instance, field, value)
    
    db.commit()
    db.refresh(instance)
    
    return instance


@router.delete("/{instance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instance(
    instance_id: str,  # <-- changed from int to str
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an instance"""
    instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
    
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Check permissions
    if not current_user.is_admin and instance.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(instance)
    db.commit()
    
    return None


@router.get("/{instance_id}/alerts", response_model=List[schemas.Alert])
async def get_instance_alerts(
    instance_id: str,  # <-- changed from int to str
    active_only: bool = True,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get alerts for an instance"""
    instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
    
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Check permissions
    if not current_user.is_admin and instance.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    query = db.query(models.Alert).filter(models.Alert.instance_id == instance_id)
    
    if active_only:
        query = query.filter(models.Alert.status == "active")
    
    alerts = query.order_by(models.Alert.triggered_at.desc()).all()
    
    return alerts