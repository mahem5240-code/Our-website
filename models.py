"""
SQLAlchemy ORM models — the database schema.

Design overview
----------------
Year            -> one row per academic year (2nd/3rd/4th Year AIML)
Faculty         -> one row per faculty member
Subject         -> a subject or lab taught in a given Year, taught by a Faculty
TimeSlot        -> a period on the daily timetable grid (also used for
                   breaks/lunch, marked with is_break / is_lunch flags)
ClassSchedule   -> the actual timetable cell: (year, day, time_slot) ->
                   subject + faculty. This is what gets read to build any
                   "view" of the timetable (by day, by year, by faculty...).

Storing the timetable as rows in ClassSchedule (instead of hardcoding
JSON in the API layer) is what makes this "structured and editable":
admins can add/update/delete individual class periods through the API.
"""

import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Enum as SAEnum,
)
from sqlalchemy.orm import relationship

from app.database.db import Base


class DayOfWeek(str, enum.Enum):
    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"


class Year(Base):
    """An academic year group, e.g. 2nd Year AIML."""

    __tablename__ = "years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g. "2nd Year AIML"
    section = Column(String(10), nullable=True)  # e.g. "A" (kept for future multi-section support)
    class_incharge = Column(String(100), nullable=True)

    subjects = relationship("Subject", back_populates="year", cascade="all, delete-orphan")
    schedules = relationship("ClassSchedule", back_populates="year", cascade="all, delete-orphan")


class Faculty(Base):
    """A faculty member who can teach one or more subjects."""

    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    subjects = relationship("Subject", back_populates="faculty")
    schedules = relationship("ClassSchedule", back_populates="faculty")


class Subject(Base):
    """
    A subject or lab. `is_lab` distinguishes a lab session (e.g. "DBMS LAB")
    from a regular lecture subject (e.g. "DBMS").
    """

    __tablename__ = "subjects"
    __table_args__ = (UniqueConstraint("code", "year_id", name="uq_subject_code_per_year"),)

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), nullable=False)  # e.g. "DBMS", "OOPJ LAB"
    full_name = Column(String(200), nullable=False)
    is_lab = Column(Boolean, default=False, nullable=False)

    year_id = Column(Integer, ForeignKey("years.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=True)

    year = relationship("Year", back_populates="subjects")
    faculty = relationship("Faculty", back_populates="subjects")
    schedules = relationship("ClassSchedule", back_populates="subject")


class TimeSlot(Base):
    """
    A period on the timetable grid, shared across all years so the grid
    lines up visually (e.g. slot 1 is 9:30-10:20 for every year).
    Breaks and lunch are also modeled as TimeSlots so the full day can be
    reconstructed from one table, with is_break / is_lunch flags marking
    the non-teaching periods.
    """

    __tablename__ = "time_slots"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(50), unique=True, nullable=False)  # e.g. "9:30 AM - 10:20 AM"
    start_time = Column(String(10), nullable=False)  # "09:30"
    end_time = Column(String(10), nullable=False)  # "10:20"
    order_index = Column(Integer, nullable=False)  # sort order left-to-right on the grid
    is_break = Column(Boolean, default=False, nullable=False)
    is_lunch = Column(Boolean, default=False, nullable=False)

    schedules = relationship("ClassSchedule", back_populates="time_slot")


class ClassSchedule(Base):
    """
    The actual timetable entry: for a given Year + Day + TimeSlot, which
    Subject is taught by which Faculty. This is the single source of truth
    the whole timetable is built from.
    """

    __tablename__ = "class_schedules"
    __table_args__ = (
        # A year cannot have two different classes in the same slot on the same day.
        UniqueConstraint("year_id", "day", "time_slot_id", name="uq_year_day_slot"),
    )

    id = Column(Integer, primary_key=True, index=True)
    year_id = Column(Integer, ForeignKey("years.id"), nullable=False)
    day = Column(SAEnum(DayOfWeek), nullable=False)
    time_slot_id = Column(Integer, ForeignKey("time_slots.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)  # null for break/lunch rows
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=True)
    room = Column(String(50), nullable=True)  # e.g. "BREAK", "LUNCH", or a room code

    year = relationship("Year", back_populates="schedules")
    time_slot = relationship("TimeSlot", back_populates="schedules")
    subject = relationship("Subject", back_populates="schedules")
    faculty = relationship("Faculty", back_populates="schedules")
