"""
CRUD endpoints for TimeSlots.

TimeSlots represent every column on the timetable grid, including
break and lunch periods (flagged via is_break / is_lunch). This is what
satisfies the "Breaks" and "Lunch" API requirements — they are just
TimeSlots with a flag set, queryable like anything else.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import TimeSlot
from app.schemas.schemas import TimeSlotCreate, TimeSlotUpdate, TimeSlotOut

router = APIRouter(prefix="/api/time-slots", tags=["Time Slots"])


@router.get("/", response_model=list[TimeSlotOut])
def list_time_slots(
    is_break: Optional[bool] = None,
    is_lunch: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    List all time slots, ordered left-to-right as they appear on the grid.
    Filter with is_break=true or is_lunch=true to get only breaks or lunch.
    """
    query = db.query(TimeSlot)
    if is_break is not None:
        query = query.filter(TimeSlot.is_break == is_break)
    if is_lunch is not None:
        query = query.filter(TimeSlot.is_lunch == is_lunch)
    return query.order_by(TimeSlot.order_index).all()


@router.get("/{time_slot_id}", response_model=TimeSlotOut)
def get_time_slot(time_slot_id: int, db: Session = Depends(get_db)):
    slot = db.query(TimeSlot).filter(TimeSlot.id == time_slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail=f"Time slot with id {time_slot_id} not found.")
    return slot


@router.post("/", response_model=TimeSlotOut, status_code=status.HTTP_201_CREATED)
def create_time_slot(payload: TimeSlotCreate, db: Session = Depends(get_db)):
    existing = db.query(TimeSlot).filter(TimeSlot.label == payload.label).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Time slot '{payload.label}' already exists.")
    slot = TimeSlot(**payload.model_dump())
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


@router.put("/{time_slot_id}", response_model=TimeSlotOut)
def update_time_slot(time_slot_id: int, payload: TimeSlotUpdate, db: Session = Depends(get_db)):
    slot = db.query(TimeSlot).filter(TimeSlot.id == time_slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail=f"Time slot with id {time_slot_id} not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(slot, field, value)
    db.commit()
    db.refresh(slot)
    return slot


@router.delete("/{time_slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_time_slot(time_slot_id: int, db: Session = Depends(get_db)):
    slot = db.query(TimeSlot).filter(TimeSlot.id == time_slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail=f"Time slot with id {time_slot_id} not found.")
    db.delete(slot)
    db.commit()
    return None
