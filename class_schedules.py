"""
CRUD endpoints for ClassSchedule — the actual timetable entries.

Every create/update goes through conflict_service.find_conflicts() first,
so it is impossible to save a schedule that double-books a section,
faculty member, or room. On conflict, the API returns 409 Conflict with
a clear explanation of what clashed.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database.db import get_db
from app.models.models import ClassSchedule, Year, TimeSlot, Subject, Faculty
from app.schemas.schemas import ClassScheduleCreate, ClassScheduleUpdate, ClassScheduleOut
from app.services import conflict_service

router = APIRouter(prefix="/api/schedules", tags=["Class Schedules"])


def _with_relations(db: Session):
    return db.query(ClassSchedule).options(
        joinedload(ClassSchedule.time_slot),
        joinedload(ClassSchedule.subject),
        joinedload(ClassSchedule.faculty),
    )


def _validate_foreign_keys(db: Session, payload) -> None:
    """Raises 400 if any referenced id does not exist."""
    if payload.year_id is not None and not db.query(Year).filter(Year.id == payload.year_id).first():
        raise HTTPException(status_code=400, detail=f"Year with id {payload.year_id} does not exist.")
    if payload.time_slot_id is not None and not db.query(TimeSlot).filter(TimeSlot.id == payload.time_slot_id).first():
        raise HTTPException(status_code=400, detail=f"Time slot with id {payload.time_slot_id} does not exist.")
    if payload.subject_id is not None and not db.query(Subject).filter(Subject.id == payload.subject_id).first():
        raise HTTPException(status_code=400, detail=f"Subject with id {payload.subject_id} does not exist.")
    if payload.faculty_id is not None and not db.query(Faculty).filter(Faculty.id == payload.faculty_id).first():
        raise HTTPException(status_code=400, detail=f"Faculty with id {payload.faculty_id} does not exist.")


@router.get("/", response_model=list[ClassScheduleOut])
def list_schedules(db: Session = Depends(get_db)):
    """List every class schedule entry in the system (all years, all days)."""
    return _with_relations(db).all()


@router.get("/{schedule_id}", response_model=ClassScheduleOut)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = _with_relations(db).filter(ClassSchedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail=f"Schedule with id {schedule_id} not found.")
    return schedule


@router.post("/", response_model=ClassScheduleOut, status_code=status.HTTP_201_CREATED)
def create_schedule(payload: ClassScheduleCreate, db: Session = Depends(get_db)):
    _validate_foreign_keys(db, payload)

    conflicts = conflict_service.find_conflicts(
        db,
        year_id=payload.year_id,
        day=payload.day,
        time_slot_id=payload.time_slot_id,
        faculty_id=payload.faculty_id,
        room=payload.room,
    )
    if conflicts:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=conflicts)

    schedule = ClassSchedule(**payload.model_dump())
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return _with_relations(db).filter(ClassSchedule.id == schedule.id).first()


@router.put("/{schedule_id}", response_model=ClassScheduleOut)
def update_schedule(schedule_id: int, payload: ClassScheduleUpdate, db: Session = Depends(get_db)):
    schedule = db.query(ClassSchedule).filter(ClassSchedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail=f"Schedule with id {schedule_id} not found.")

    _validate_foreign_keys(db, payload)

    # Merge existing values with the incoming partial update before conflict-checking,
    # so we check the *resulting* state of the schedule, not just the changed fields.
    merged = {
        "year_id": payload.year_id if payload.year_id is not None else schedule.year_id,
        "day": payload.day if payload.day is not None else schedule.day,
        "time_slot_id": payload.time_slot_id if payload.time_slot_id is not None else schedule.time_slot_id,
        "faculty_id": payload.faculty_id if payload.faculty_id is not None else schedule.faculty_id,
        "room": payload.room if payload.room is not None else schedule.room,
    }

    conflicts = conflict_service.find_conflicts(
        db,
        year_id=merged["year_id"],
        day=merged["day"],
        time_slot_id=merged["time_slot_id"],
        faculty_id=merged["faculty_id"],
        room=merged["room"],
        exclude_schedule_id=schedule_id,
    )
    if conflicts:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=conflicts)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(schedule, field, value)
    db.commit()
    db.refresh(schedule)
    return _with_relations(db).filter(ClassSchedule.id == schedule.id).first()


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(ClassSchedule).filter(ClassSchedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail=f"Schedule with id {schedule_id} not found.")
    db.delete(schedule)
    db.commit()
    return None
