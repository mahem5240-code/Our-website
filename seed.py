"""
Seed data — transcribed from the Trinity College of Engineering &
Technology, Dept. of AIML timetable (W.E.F. 06-JULY-2026).

This populates:
  - 3 Years (2nd, 3rd, 4th Year AIML) with their class incharges
  - Faculty members named in each year's subject list
  - Subjects/labs per year, linked to their faculty
  - The shared TimeSlot grid (periods + break + lunch)
  - ClassSchedule entries for every day, reconstructing each year's grid

Note: the three years use different time grids (2nd & 3rd year share one
9:30-4:00 structure with a break after period 4 and lunch after period 5;
4th year's grid differs slightly in break/lunch placement), so each year
gets its own TimeSlot set to stay faithful to the source image.
"""

from sqlalchemy.orm import Session

from app.models.models import Year, Faculty, Subject, TimeSlot, ClassSchedule, DayOfWeek

D = DayOfWeek


def seed_if_empty(db: Session) -> None:
    if db.query(Year).count() > 0:
        return  # already seeded
    _seed(db)


def _get_or_create_faculty(db: Session, cache: dict, name: str) -> Faculty:
    if name in cache:
        return cache[name]
    faculty = Faculty(name=name)
    db.add(faculty)
    db.flush()
    cache[name] = faculty
    return faculty


def _seed(db: Session) -> None:
    faculty_cache: dict[str, Faculty] = {}

    # -----------------------------------------------------------------
    # YEARS
    # -----------------------------------------------------------------
    year2 = Year(name="2nd Year AIML", section="A", class_incharge="Mrs. Tarannum Fatima")
    year3 = Year(name="3rd Year AIML", section="A", class_incharge="Mrs. P. Lavanya")
    year4 = Year(name="4th Year AIML", section="A", class_incharge="Mr. SD. Khaja Pasha")
    db.add_all([year2, year3, year4])
    db.flush()

    # -----------------------------------------------------------------
    # TIME SLOTS — shared grid for 2nd & 3rd year:
    # 9:30-10:20, 10:20-11:10, 11:10-11:20 (SHORT BREAK "BREAK"),
    # 11:20-12:10, 12:10-1:00, 1:00-1:45 (LUNCH),
    # 1:45-2:30, 2:30-3:15, 3:15-4:00
    # -----------------------------------------------------------------
    slots_23 = [
        TimeSlot(label="9:30 AM - 10:20 AM", start_time="09:30", end_time="10:20", order_index=1),
        TimeSlot(label="10:20 AM - 11:10 AM", start_time="10:20", end_time="11:10", order_index=2),
        TimeSlot(label="11:10 AM - 11:20 AM", start_time="11:10", end_time="11:20", order_index=3, is_break=True),
        TimeSlot(label="11:20 AM - 12:10 PM", start_time="11:20", end_time="12:10", order_index=4),
        TimeSlot(label="12:10 PM - 01:00 PM", start_time="12:10", end_time="13:00", order_index=5),
        TimeSlot(label="01:00 PM - 01:45 PM", start_time="13:00", end_time="13:45", order_index=6, is_lunch=True),
        TimeSlot(label="01:45 PM - 02:30 PM", start_time="13:45", end_time="14:30", order_index=7),
        TimeSlot(label="02:30 PM - 03:15 PM", start_time="14:30", end_time="15:15", order_index=8),
        TimeSlot(label="03:15 PM - 04:00 PM", start_time="15:15", end_time="16:00", order_index=9),
    ]
    db.add_all(slots_23)
    db.flush()
    s = {slot.order_index: slot for slot in slots_23}  # slots for year 2 & 3

    # -----------------------------------------------------------------
    # FACULTY (2nd Year)
    # -----------------------------------------------------------------
    f_naga_laxmi = _get_or_create_faculty(db, faculty_cache, "Mrs. K. Naga Laxmi")
    f_glakshimi = _get_or_create_faculty(db, faculty_cache, "G. Lakshimi")
    f_tarannum = _get_or_create_faculty(db, faculty_cache, "Tarannum Fatima")
    f_plavanya = _get_or_create_faculty(db, faculty_cache, "P. Lavanya")
    f_khaja = _get_or_create_faculty(db, faculty_cache, "Syed Khaja Pasha")
    f_manighanesh = _get_or_create_faculty(db, faculty_cache, "Dr. Mani Ganesh")

    # -----------------------------------------------------------------
    # SUBJECTS (2nd Year) — codes/names/faculty per the right-hand table
    # -----------------------------------------------------------------
    sub2 = {
        "MSF": Subject(code="MSF", full_name="MSF", year_id=year2.id, faculty_id=f_naga_laxmi.id),
        "OOPJ": Subject(code="OOPJ", full_name="OOPJ", year_id=year2.id, faculty_id=f_glakshimi.id),
        "COA": Subject(code="COA", full_name="COA", year_id=year2.id, faculty_id=f_tarannum.id),
        "SE": Subject(code="SE", full_name="SE", year_id=year2.id, faculty_id=f_plavanya.id),
        "DBMS": Subject(code="DBMS", full_name="DBMS", year_id=year2.id, faculty_id=f_khaja.id),
        "DBMS LAB": Subject(code="DBMS LAB", full_name="DBMS Lab", is_lab=True, year_id=year2.id, faculty_id=f_khaja.id),
        "SE LAB": Subject(code="SE LAB", full_name="SE Lab", is_lab=True, year_id=year2.id, faculty_id=f_plavanya.id),
        "NODE JS LAB": Subject(code="NODE JS LAB", full_name="Node JS Lab", is_lab=True, year_id=year2.id, faculty_id=f_glakshimi.id),
        "CM LAB": Subject(code="CM LAB", full_name="CM Lab", is_lab=True, year_id=year2.id, faculty_id=f_manighanesh.id),
        "OOPJ LAB": Subject(code="OOPJ LAB", full_name="OOPJ Lab", is_lab=True, year_id=year2.id, faculty_id=f_glakshimi.id),
    }
    db.add_all(sub2.values())
    db.flush()

    # -----------------------------------------------------------------
    # SCHEDULE (2nd Year) — transcribed cell-by-cell from the grid.
    # Columns: 1=9:30,2=10:20,3=BREAK,4=11:20,5=12:10,6=LUNCH,7=1:45,8=2:30,9=3:15
    # -----------------------------------------------------------------
    def row(day, entries):
        """entries: dict of order_index -> subject_code (or None for free)."""
        for idx, code in entries.items():
            subj = sub2.get(code) if code else None
            db.add(ClassSchedule(
                year_id=year2.id, day=day, time_slot_id=s[idx].id,
                subject_id=subj.id if subj else None,
                faculty_id=subj.faculty_id if subj else None,
                room="BREAK" if s[idx].is_break else ("LUNCH" if s[idx].is_lunch else None),
            ))

    row(D.MON, {1: "DBMS", 2: "OOPJ LAB", 4: "OOPJ LAB", 5: "OOPJ LAB", 7: "SE", 8: "OOPJ", 9: "MSF"})
    row(D.TUE, {1: "MSF", 2: "NODE JS LAB", 4: "NODE JS LAB", 5: "NODE JS LAB", 7: "SE", 8: "COA", 9: "DBMS"})
    row(D.WED, {1: "OOPJ", 2: "MSF", 4: "COA", 5: "COA", 7: "SE", 8: "SE", 9: "OOPJ"})
    row(D.THU, {1: "COA", 2: "OOPJ", 4: "OOPJ", 5: "DBMS", 7: "CM LAB", 8: "CM LAB", 9: "CM LAB"})
    row(D.FRI, {1: "MSF", 2: "DBMS LAB", 4: "DBMS LAB", 5: "DBMS LAB", 7: "COA", 8: "DBMS", 9: "MSF"})
    row(D.SAT, {1: "DBMS", 2: "SE LAB", 4: "SE LAB", 5: "SE LAB", 7: "MSF", 8: "SE", 9: "COA"})

    # -----------------------------------------------------------------
    # FACULTY (3rd Year)
    # -----------------------------------------------------------------
    f_vidyasagar = _get_or_create_faculty(db, faculty_cache, "G. Vidyasagar")
    f_arifarfath = _get_or_create_faculty(db, faculty_cache, "Dr. Arif Arfath")
    f_sdkhaja = _get_or_create_faculty(db, faculty_cache, "SD. Khaja Pasha")
    f_braju = _get_or_create_faculty(db, faculty_cache, "B. Raju")

    # -----------------------------------------------------------------
    # SUBJECTS (3rd Year)
    # -----------------------------------------------------------------
    sub3 = {
        "DAA": Subject(code="DAA", full_name="DAA", year_id=year3.id, faculty_id=f_tarannum.id),
        "ML": Subject(code="ML", full_name="ML", year_id=year3.id, faculty_id=f_vidyasagar.id),
        "CN": Subject(code="CN", full_name="CN", year_id=year3.id, faculty_id=f_plavanya.id),
        "BEFA": Subject(code="BEFA", full_name="BEFA", year_id=year3.id, faculty_id=f_arifarfath.id),
        "WP": Subject(code="WP", full_name="WP", year_id=year3.id, faculty_id=f_sdkhaja.id),
        "ML LAB": Subject(code="ML LAB", full_name="ML Lab", is_lab=True, year_id=year3.id, faculty_id=f_vidyasagar.id),
        "AECS LAB": Subject(code="AECS LAB", full_name="AECS Lab", is_lab=True, year_id=year3.id, faculty_id=f_braju.id),
        "CN LAB": Subject(code="CN LAB", full_name="CN Lab", is_lab=True, year_id=year3.id, faculty_id=f_plavanya.id),
        "FLUTTER": Subject(code="FLUTTER", full_name="Flutter Lab", is_lab=True, year_id=year3.id, faculty_id=None),
    }
    db.add_all(sub3.values())
    db.flush()

    def row3(day, entries):
        for idx, code in entries.items():
            subj = sub3.get(code) if code else None
            db.add(ClassSchedule(
                year_id=year3.id, day=day, time_slot_id=s[idx].id,
                subject_id=subj.id if subj else None,
                faculty_id=subj.faculty_id if subj else None,
                room="BREAK" if s[idx].is_break else ("LUNCH" if s[idx].is_lunch else None),
            ))

    # NOTE: 3rd year's grid has "B R E A K" spanning the mid-morning column
    # (period 3) same as the break slot, and a BREAK row (not lunch) placed
    # between THU/FRI in the source image labelled "BREAK" as its own row
    # for Thursday's second half — modeled here using the shared break slot.
    row3(D.MON, {1: "DAA", 2: "ML", 4: "CN", 5: "WP", 7: "ML", 8: "BEFA", 9: "WP"})
    row3(D.TUE, {1: "DAA", 2: "WP", 4: "CN", 5: "ML", 7: "ML LAB", 8: "ML LAB", 9: "ML LAB"})
    row3(D.WED, {1: "DAA", 2: "ML", 4: "WP", 5: "CN", 7: "AECS LAB", 8: "AECS LAB", 9: "AECS LAB"})
    row3(D.THU, {1: "WP", 2: "WP", 4: "CN", 5: "WP", 7: "DAA", 8: "CN", 9: "BEFA"})
    row3(D.FRI, {1: "DAA", 2: "BEFA", 4: "CN", 5: "WP", 7: "CN", 8: "CN", 9: "CN"})
    row3(D.SAT, {1: "CN", 2: "ML", 4: "WP", 5: "DAA", 7: "CN", 8: "BEFA", 9: "ML"})

    # -----------------------------------------------------------------
    # 4TH YEAR — this grid's break/lunch columns sit in different
    # positions than years 2 & 3 (break after period 2, lunch after
    # period 4), so it gets its own TimeSlot set.
    # -----------------------------------------------------------------
    slots_4 = [
        TimeSlot(label="9:30 AM - 10:20 AM (Y4)", start_time="09:30", end_time="10:20", order_index=101),
        TimeSlot(label="10:20 AM - 11:10 AM (Y4)", start_time="10:20", end_time="11:10", order_index=102),
        TimeSlot(label="11:10 AM - 11:20 AM (Y4)", start_time="11:10", end_time="11:20", order_index=103, is_break=True),
        TimeSlot(label="11:20 AM - 12:10 PM (Y4)", start_time="11:20", end_time="12:10", order_index=104),
        TimeSlot(label="12:10 PM - 01:00 PM (Y4)", start_time="12:10", end_time="13:00", order_index=105),
        TimeSlot(label="01:00 PM - 01:45 PM (Y4)", start_time="13:00", end_time="13:45", order_index=106, is_lunch=True),
        TimeSlot(label="01:45 PM - 02:30 PM (Y4)", start_time="13:45", end_time="14:30", order_index=107),
        TimeSlot(label="02:30 PM - 03:15 PM (Y4)", start_time="14:30", end_time="15:15", order_index=108),
        TimeSlot(label="03:15 PM - 04:00 PM (Y4)", start_time="15:15", end_time="16:00", order_index=109),
    ]
    db.add_all(slots_4)
    db.flush()
    s4 = {slot.order_index - 100: slot for slot in slots_4}

    f_ashok = _get_or_create_faculty(db, faculty_cache, "K. Ashok")

    sub4 = {
        "DL": Subject(code="DL", full_name="DL", year_id=year4.id, faculty_id=f_glakshimi.id),
        "NIC": Subject(code="NIC", full_name="NIC", year_id=year4.id, faculty_id=f_ashok.id),
        "CC": Subject(code="CC", full_name="CC", year_id=year4.id, faculty_id=f_plavanya.id),
        "SW": Subject(code="SW", full_name="SW", year_id=year4.id, faculty_id=f_sdkhaja.id),
        "DM": Subject(code="DM", full_name="DM", year_id=year4.id, faculty_id=f_tarannum.id),
        "PPLE": Subject(code="PPLE", full_name="PPLE", year_id=year4.id, faculty_id=None),
        "CC LAB": Subject(code="CC LAB", full_name="CC Lab", is_lab=True, year_id=year4.id, faculty_id=f_plavanya.id),
        "SOFTSKILLS": Subject(code="SOFTSKILLS", full_name="Soft Skills", is_lab=True, year_id=year4.id, faculty_id=None),
        "PROJECT STAGE-I": Subject(code="PROJECT STAGE-I", full_name="Project Stage - I", year_id=year4.id, faculty_id=None),
    }
    db.add_all(sub4.values())
    db.flush()

    def row4(day, entries):
        for idx, code in entries.items():
            subj = sub4.get(code) if code else None
            db.add(ClassSchedule(
                year_id=year4.id, day=day, time_slot_id=s4[idx].id,
                subject_id=subj.id if subj else None,
                faculty_id=subj.faculty_id if subj else None,
                room="BREAK" if s4[idx].is_break else ("LUNCH" if s4[idx].is_lunch else None),
            ))

    row4(D.MON, {1: "CC", 2: "NIC", 4: "DM", 5: "DM", 7: "DL", 8: "CC", 9: "PPLE"})
    row4(D.TUE, {1: "CC", 2: "NIC", 4: "NIC", 5: "SW", 7: "DM", 8: "DL", 9: "PPLE"})
    row4(D.WED, {1: "CC", 2: "CC LAB", 4: "CC LAB", 5: "CC LAB", 7: "DL", 8: "SW", 9: "PPLE"})
    row4(D.THU, {1: "CC", 2: "NIC", 4: "DM", 5: "DL", 7: "PROJECT STAGE-I", 8: "PROJECT STAGE-I", 9: "PPLE"})
    row4(D.FRI, {1: "CC", 2: "NIC", 4: "DM", 5: "DL", 7: "SOFTSKILLS", 8: "SOFTSKILLS", 9: "PPLE"})
    row4(D.SAT, {1: "DL", 2: "NIC", 4: "DM", 5: "SW"})

    db.commit()
