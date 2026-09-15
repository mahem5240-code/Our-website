"""CRUD endpoints for Faculty members."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import Faculty
from app.schemas.schemas import FacultyCreate, FacultyUpdate, FacultyOut

router = APIRouter(prefix="/api/faculty", tags=["Faculty"])


@router.get("/", response_model=list[FacultyOut])
def list_faculty(db: Session = Depends(get_db)):
    return db.query(Faculty).all()


@router.get("/{faculty_id}", response_model=FacultyOut)
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail=f"Faculty with id {faculty_id} not found.")
    return faculty


@router.post("/", response_model=FacultyOut, status_code=status.HTTP_201_CREATED)
def create_faculty(payload: FacultyCreate, db: Session = Depends(get_db)):
    existing = db.query(Faculty).filter(Faculty.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Faculty '{payload.name}' already exists.")
    faculty = Faculty(**payload.model_dump())
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return faculty


@router.put("/{faculty_id}", response_model=FacultyOut)
def update_faculty(faculty_id: int, payload: FacultyUpdate, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail=f"Faculty with id {faculty_id} not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(faculty, field, value)
    db.commit()
    db.refresh(faculty)
    return faculty


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail=f"Faculty with id {faculty_id} not found.")
    db.delete(faculty)
    db.commit()
    return None
