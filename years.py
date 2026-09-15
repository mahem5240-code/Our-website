"""CRUD endpoints for academic Years (2nd/3rd/4th Year AIML)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import Year
from app.schemas.schemas import YearCreate, YearUpdate, YearOut

router = APIRouter(prefix="/api/years", tags=["Years"])


@router.get("/", response_model=list[YearOut])
def list_years(db: Session = Depends(get_db)):
    """Return all academic years."""
    return db.query(Year).all()


@router.get("/{year_id}", response_model=YearOut)
def get_year(year_id: int, db: Session = Depends(get_db)):
    year = db.query(Year).filter(Year.id == year_id).first()
    if not year:
        raise HTTPException(status_code=404, detail=f"Year with id {year_id} not found.")
    return year


@router.post("/", response_model=YearOut, status_code=status.HTTP_201_CREATED)
def create_year(payload: YearCreate, db: Session = Depends(get_db)):
    existing = db.query(Year).filter(Year.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Year '{payload.name}' already exists.")
    year = Year(**payload.model_dump())
    db.add(year)
    db.commit()
    db.refresh(year)
    return year


@router.put("/{year_id}", response_model=YearOut)
def update_year(year_id: int, payload: YearUpdate, db: Session = Depends(get_db)):
    year = db.query(Year).filter(Year.id == year_id).first()
    if not year:
        raise HTTPException(status_code=404, detail=f"Year with id {year_id} not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(year, field, value)
    db.commit()
    db.refresh(year)
    return year


@router.delete("/{year_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_year(year_id: int, db: Session = Depends(get_db)):
    year = db.query(Year).filter(Year.id == year_id).first()
    if not year:
        raise HTTPException(status_code=404, detail=f"Year with id {year_id} not found.")
    db.delete(year)
    db.commit()
    return None
