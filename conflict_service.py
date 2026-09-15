"""
Conflict detection service.

Encapsulates the business rules that prevent invalid timetables:
  1. Section conflict  -> the same Year already has a class in that
                           Day + TimeSlot (a year can't have two classes
                           at once).
  2. Faculty conflict   -> the same Faculty is already teaching a
                           DIFFERENT year in that Day + TimeSlot (a
                           teacher can't be in two places at once).
  3. Room conflict      -> the same room is already booked in that
                           Day + TimeSlot (only checked when a room is
                           actually supplied).

Kept separate from the router so the same checks can be reused by the
create endpoint, the update endpoint, and any future bulk-import tool.
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.models import ClassSchedule, DayOfWeek


def find_conflicts(
    db: Session,
    year_id: int,
    day: DayOfWeek,
    time_slot_id: int,
    faculty_id: Optional[int] = None,
    room: Optional[str] = None,
    exclude_schedule_id: Optional[int] = None,
) -> list[str]:
    """
    Returns a list of human-readable conflict descriptions.
    An empty list means the proposed schedule entry is safe to save.

    `exclude_schedule_id` is used when updating an existing entry, so it
    doesn't flag a conflict with itself.
    """
    conflicts: list[str] = []

    base_query = db.query(ClassSchedule).filter(
        ClassSchedule.day == day,
        ClassSchedule.time_slot_id == time_slot_id,
    )
    if exclude_schedule_id is not None:
        base_query = base_query.filter(ClassSchedule.id != exclude_schedule_id)

    # 1. Section conflict: this year already has something scheduled here.
    section_clash = base_query.filter(ClassSchedule.year_id == year_id).first()
    if section_clash:
        conflicts.append(
            f"Section conflict: Year id={year_id} already has a class scheduled "
            f"on {day.value} in this time slot (schedule id={section_clash.id})."
        )

    # 2. Faculty conflict: same faculty double-booked across different years.
    if faculty_id is not None:
        faculty_clash = base_query.filter(
            ClassSchedule.faculty_id == faculty_id,
            ClassSchedule.year_id != year_id,
        ).first()
        if faculty_clash:
            conflicts.append(
                f"Faculty conflict: Faculty id={faculty_id} is already teaching "
                f"Year id={faculty_clash.year_id} on {day.value} in this time slot "
                f"(schedule id={faculty_clash.id})."
            )

    # 3. Room conflict: same room double-booked.
    if room:
        room_clash = base_query.filter(
            ClassSchedule.room == room,
            ClassSchedule.year_id != year_id,
        ).first()
        if room_clash:
            conflicts.append(
                f"Room conflict: Room '{room}' is already booked by Year "
                f"id={room_clash.year_id} on {day.value} in this time slot "
                f"(schedule id={room_clash.id})."
            )

    return conflicts
