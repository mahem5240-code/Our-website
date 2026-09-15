"""
Pydantic schemas — request/response validation models.

Naming convention used throughout this file:
  *Base     -> shared fields
  *Create   -> fields required to create a new record (input)
  *Update   -> fields allowed when updating a record (input, all optional)
  *Out      -> fields returned to the client (output), includes `id`
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

from app.models.models import DayOfWeek


# ---------------------------------------------------------------------------
# Year
# ---------------------------------------------------------------------------

class YearBase(BaseModel):
    name: str
    section: Optional[str] = None
    class_incharge: Optional[str] = None


class YearCreate(YearBase):
    pass


class YearUpdate(BaseModel):
    name: Optional[str] = None
    section: Optional[str] = None
    class_incharge: Optional[str] = None


class YearOut(YearBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------------------------------------
# Faculty
# ---------------------------------------------------------------------------

class FacultyBase(BaseModel):
    name: str


class FacultyCreate(FacultyBase):
    pass


class FacultyUpdate(BaseModel):
    name: Optional[str] = None


class FacultyOut(FacultyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------------------------------------
# Subject
# ---------------------------------------------------------------------------

class SubjectBase(BaseModel):
    code: str
    full_name: str
    is_lab: bool = False
    year_id: int
    faculty_id: Optional[int] = None


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    code: Optional[str] = None
    full_name: Optional[str] = None
    is_lab: Optional[bool] = None
    year_id: Optional[int] = None
    faculty_id: Optional[int] = None


class SubjectOut(SubjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    faculty: Optional[FacultyOut] = None


# ---------------------------------------------------------------------------
# TimeSlot
# ---------------------------------------------------------------------------

class TimeSlotBase(BaseModel):
    label: str
    start_time: str
    end_time: str
    order_index: int
    is_break: bool = False
    is_lunch: bool = False


class TimeSlotCreate(TimeSlotBase):
    pass


class TimeSlotUpdate(BaseModel):
    label: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    order_index: Optional[int] = None
    is_break: Optional[bool] = None
    is_lunch: Optional[bool] = None


class TimeSlotOut(TimeSlotBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------------------------------------
# ClassSchedule
# ---------------------------------------------------------------------------

class ClassScheduleBase(BaseModel):
    year_id: int
    day: DayOfWeek
    time_slot_id: int
    subject_id: Optional[int] = None
    faculty_id: Optional[int] = None
    room: Optional[str] = None


class ClassScheduleCreate(ClassScheduleBase):
    pass


class ClassScheduleUpdate(BaseModel):
    year_id: Optional[int] = None
    day: Optional[DayOfWeek] = None
    time_slot_id: Optional[int] = None
    subject_id: Optional[int] = None
    faculty_id: Optional[int] = None
    room: Optional[str] = None


class ClassScheduleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    year_id: int
    day: DayOfWeek
    room: Optional[str] = None
    time_slot: TimeSlotOut
    subject: Optional[SubjectOut] = None
    faculty: Optional[FacultyOut] = None


# ---------------------------------------------------------------------------
# Conflict-check helper schema
# ---------------------------------------------------------------------------

class ConflictCheckResult(BaseModel):
    has_conflict: bool
    conflicts: list[str] = []
