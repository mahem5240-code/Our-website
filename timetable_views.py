"""
Read-only "view" endpoints that answer the common questions students and
faculty actually ask: what's the full week look like, what's on today,
what does this professor teach, what's my next class, etc.

All of these are built on top of ClassSchedule via timetable_service —
no data is duplicated or hardcoded here, it's all queried live.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import Year, Subject, Faculty, DayOfWeek
from app.schemas.schemas import ClassScheduleOut
from app.services import timetable_service

router = APIRouter(prefix="/api/timetable", tags=["Timetable Views"])


@router.get("/year/{year_id}/weekly", response_model=list[ClassScheduleOut])
def weekly_timetable(year_id: int, db: Session = Depends(get_db)):
    """Complete weekly timetable for one year (all days, in order)."""
    if not db.query(Year).filter(Year.id == year_id).first():
        raise HTTPException(status_code=404, detail=f"Year with id {year_id} not found.")
    return timetable_service.get_weekly_timetable(db, year_id)


@router.get("/year/{year_id}/day/{day}", response_model=list[ClassScheduleOut])
def timetable_by_day(year_id: int, day: DayOfWeek, db: Session = Depends(get_db)):
    """Timetable for one year on a single day, e.g. MON."""
    if not db.query(Year).filter(Year.id == year_id).first():
        raise HTTPException(status_code=404, detail=f"Year with id {year_id} not found.")
    return timetable_service.get_timetable_by_day(db, year_id, day)


@router.get("/year/{year_id}", response_model=list[ClassScheduleOut])
def timetable_by_year(year_id: int, db: Session = Depends(get_db)):
    """Alias for the full weekly timetable of a year (same as /weekly)."""
    if not db.query(Year).filter(Year.id == year_id).first():
        raise HTTPException(status_code=404, detail=f"Year with id {year_id} not found.")
    return timetable_service.get_weekly_timetable(db, year_id)


@router.get("/subject/{subject_id}", response_model=list[ClassScheduleOut])
def timetable_by_subject(subject_id: int, db: Session = Depends(get_db)):
    """Every scheduled slot for a given subject across the week."""
    if not db.query(Subject).filter(Subject.id == subject_id).first():
        raise HTTPException(status_code=404, detail=f"Subject with id {subject_id} not found.")
    return timetable_service.get_timetable_by_subject(db, subject_id)


@router.get("/faculty/{faculty_id}", response_model=list[ClassScheduleOut])
def timetable_by_faculty(faculty_id: int, db: Session = Depends(get_db)):
    """Every class a given faculty member teaches across the week."""
    if not db.query(Faculty).filter(Faculty.id == faculty_id).first():
        raise HTTPException(status_code=404, detail=f"Faculty with id {faculty_id} not found.")
    return timetable_service.get_timetable_by_faculty(db, faculty_id)


@router.get("/year/{year_id}/current-next")
def current_and_next_class(year_id: int, db: Session = Depends(get_db)):
    """
    Returns the class happening right now (if any) and the next upcoming
    class for a given year, based on the server's current date/time.
    """
    if not db.query(Year).filter(Year.id == year_id).first():
        raise HTTPException(status_code=404, detail=f"Year with id {year_id} not found.")

    result = timetable_service.get_current_and_next_class(db, year_id)

    def serialize(entry):
        return ClassScheduleOut.model_validate(entry) if entry else None

    return {
        "current_class": serialize(result["current"]),
        "next_class": serialize(result["next"]),
    }
