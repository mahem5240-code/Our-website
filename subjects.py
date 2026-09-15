"""CRUD endpoints for Subjects (and Labs, which are Subjects with is_lab=True)."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database.db import get_db
from app.models.models import Subject, Year, Faculty
from app.schemas.schemas import SubjectCreate, SubjectUpdate, SubjectOut

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])


@router.get("/", response_model=list[SubjectOut])
def list_subjects(
    year_id: Optional[int] = None,
    is_lab: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    List subjects, optionally filtered by year and/or lab status.
    e.g. GET /api/subjects/?year_id=2&is_lab=true lists only labs for that year.
    """
    query = db.query(Subject).options(joinedload(Subject.faculty))
    if year_id is not None:
        query = query.filter(Subject.year_id == year_id)
    if is_lab is not None:
        query = query.filter(Subject.is_lab == is_lab)
    return query.all()


@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = (
        db.query(Subject)
        .options(joinedload(Subject.faculty))
        .filter(Subject.id == subject_id)
        .first()
    )
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject with id {subject_id} not found.")
    return subject


@router.post("/", response_model=SubjectOut, status_code=status.HTTP_201_CREATED)
def create_subject(payload: SubjectCreate, db: Session = Depends(get_db)):
    if not db.query(Year).filter(Year.id == payload.year_id).first():
        raise HTTPException(status_code=400, detail=f"Year with id {payload.year_id} does not exist.")
    if payload.faculty_id is not None and not db.query(Faculty).filter(Faculty.id == payload.faculty_id).first():
        raise HTTPException(status_code=400, detail=f"Faculty with id {payload.faculty_id} does not exist.")

    existing = (
        db.query(Subject)
        .filter(Subject.code == payload.code, Subject.year_id == payload.year_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Subject code '{payload.code}' already exists for this year.",
        )

    subject = Subject(**payload.model_dump())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.put("/{subject_id}", response_model=SubjectOut)
def update_subject(subject_id: int, payload: SubjectUpdate, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject with id {subject_id} not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(subject, field, value)
    db.commit()
    db.refresh(subject)
    return subject


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject with id {subject_id} not found.")
    db.delete(subject)
    db.commit()
    return None
