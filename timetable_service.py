"""
Timetable query service.

Holds the reusable read-queries that power the various "view" endpoints
(by day, by year, by subject, by faculty, current/next class...). Keeping
these out of the router functions makes the router layer thin and keeps
all query logic in one testable place.
"""

from datetime import datetime, date, time
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.models.models import ClassSchedule, TimeSlot, DayOfWeek


def _base_schedule_query(db: Session):
    """A ClassSchedule query with all related objects eagerly loaded."""
    return db.query(ClassSchedule).options(
        joinedload(ClassSchedule.time_slot),
        joinedload(ClassSchedule.subject),
        joinedload(ClassSchedule.faculty),
    )


def get_weekly_timetable(db: Session, year_id: int) -> list[ClassSchedule]:
    """Full week of classes for one year, ordered by day then time slot."""
    return (
        _base_schedule_query(db)
        .filter(ClassSchedule.year_id == year_id)
        .join(TimeSlot)
        .order_by(ClassSchedule.day, TimeSlot.order_index)
        .all()
    )


def get_timetable_by_day(db: Session, year_id: int, day: DayOfWeek) -> list[ClassSchedule]:
    """One day's classes for one year, ordered by time slot."""
    return (
        _base_schedule_query(db)
        .filter(ClassSchedule.year_id == year_id, ClassSchedule.day == day)
        .join(TimeSlot)
        .order_by(TimeSlot.order_index)
        .all()
    )


def get_timetable_by_subject(db: Session, subject_id: int) -> list[ClassSchedule]:
    """Every scheduled occurrence of a given subject, across the week."""
    return (
        _base_schedule_query(db)
        .filter(ClassSchedule.subject_id == subject_id)
        .join(TimeSlot)
        .order_by(ClassSchedule.day, TimeSlot.order_index)
        .all()
    )


def get_timetable_by_faculty(db: Session, faculty_id: int) -> list[ClassSchedule]:
    """Every class a given faculty member teaches, across the week."""
    return (
        _base_schedule_query(db)
        .filter(ClassSchedule.faculty_id == faculty_id)
        .join(TimeSlot)
        .order_by(ClassSchedule.day, TimeSlot.order_index)
        .all()
    )


_DAY_ORDER = [
    DayOfWeek.MON,
    DayOfWeek.TUE,
    DayOfWeek.WED,
    DayOfWeek.THU,
    DayOfWeek.FRI,
    DayOfWeek.SAT,
]


def _parse_hhmm(value: str) -> time:
    """Parses a 'HH:MM' 24-hour string into a datetime.time object."""
    hour, minute = value.split(":")
    return time(hour=int(hour), minute=int(minute))


def get_current_and_next_class(
    db: Session, year_id: int, now: Optional[datetime] = None
) -> dict:
    """
    Determines the current class (if any) and the next upcoming class for
    a year, based on the current day of week and time of day.

    Returns a dict: {"current": ClassSchedule | None, "next": ClassSchedule | None}
    """
    now = now or datetime.now()
    today_index = now.weekday()  # Monday=0 ... Sunday=6

    if today_index > 5:
        # Sunday: no classes. Next class is Monday's first period.
        current = None
        next_class = _first_class_of_day(db, year_id, DayOfWeek.MON)
        return {"current": current, "next": next_class}

    today = _DAY_ORDER[today_index]
    todays_schedule = get_timetable_by_day(db, year_id, today)

    current = None
    next_class = None
    now_time = now.time()

    for entry in todays_schedule:
        start = _parse_hhmm(entry.time_slot.start_time)
        end = _parse_hhmm(entry.time_slot.end_time)
        if start <= now_time < end:
            current = entry
        elif start > now_time and next_class is None:
            next_class = entry

    # If nothing left today, look ahead to the next day that has classes.
    # Days cycle MON..SAT (Sunday is skipped, since the college has no classes then).
    if next_class is None:
        for offset in range(1, 7):
            candidate_day = _DAY_ORDER[(today_index + offset) % 6]
            candidate = _first_class_of_day(db, year_id, candidate_day)
            if candidate:
                next_class = candidate
                break

    return {"current": current, "next": next_class}


def _first_class_of_day(db: Session, year_id: int, day: DayOfWeek) -> Optional[ClassSchedule]:
    schedule = get_timetable_by_day(db, year_id, day)
    return schedule[0] if schedule else None
