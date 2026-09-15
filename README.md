# College AIML Timetable Management System — Backend

A clean, production-ready FastAPI backend for managing the AIML department's
2nd, 3rd, and 4th Year timetables (Trinity College of Engineering &
Technology, Peddapalli — transcribed from the W.E.F. 06-JULY-2026 timetable).

## Project structure

```
app/
├── main.py                  # FastAPI app, CORS, startup seeding, router wiring
├── config.py                 # Environment-based settings
├── database/
│   ├── db.py                 # SQLAlchemy engine/session
│   └── seed.py                # Seed data transcribed from the timetable image
├── models/
│   └── models.py              # SQLAlchemy ORM models (schema)
├── schemas/
│   └── schemas.py              # Pydantic request/response models
├── services/
│   ├── conflict_service.py     # Faculty/section/room conflict detection
│   └── timetable_service.py    # Weekly/day/subject/faculty/current-next queries
└── routers/
    ├── years.py                 # /api/years
    ├── faculty.py                 # /api/faculty
    ├── subjects.py                 # /api/subjects  (labs are subjects with is_lab=true)
    ├── time_slots.py                # /api/time-slots (breaks/lunch are slots with flags)
    ├── class_schedules.py             # /api/schedules (CRUD + conflict checks)
    └── timetable_views.py              # /api/timetable/... (read-only views)
```

## Database schema (entity overview)

- **Year** — 2nd/3rd/4th Year AIML, with class incharge
- **Faculty** — faculty members
- **Subject** — a subject or lab (`is_lab` flag), belongs to a Year, taught by a Faculty
- **TimeSlot** — one column of the timetable grid (also breaks/lunch via `is_break`/`is_lunch`)
- **ClassSchedule** — the actual cell: (Year, Day, TimeSlot) → Subject + Faculty + Room

Storing the timetable as `ClassSchedule` rows (rather than hardcoding it into
API responses) is what makes it structured and editable — every class period
can be created, updated, or deleted through the API.

## Setup & run (local)

**Requirements:** Python 3.10+

```bash
# 1. Clone / unzip the project, then enter it
cd timetable-backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment config
cp .env.example .env
# (defaults work out of the box with SQLite — no edits needed for local dev)

# 5. Run the server
uvicorn app.main:app --reload
```

The API will be live at **http://127.0.0.1:8000**

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

On first startup, the database is automatically created and seeded with the
full 2nd/3rd/4th Year timetable data (controlled by `AUTO_SEED=true` in `.env`).

## Key API endpoints

| Purpose                         | Endpoint                                          |
|----------------------------------|----------------------------------------------------|
| List years                       | `GET /api/years/`                                   |
| List faculty                     | `GET /api/faculty/`                                  |
| List subjects (filter by year/lab)| `GET /api/subjects/?year_id=1&is_lab=true`           |
| List time slots (filter break/lunch)| `GET /api/time-slots/?is_break=true`               |
| Create a schedule entry (conflict-checked)| `POST /api/schedules/`                       |
| Full weekly timetable for a year  | `GET /api/timetable/year/{year_id}/weekly`           |
| Timetable for one day             | `GET /api/timetable/year/{year_id}/day/{day}` (day = MON..SAT) |
| Timetable by subject              | `GET /api/timetable/subject/{subject_id}`            |
| Timetable by faculty              | `GET /api/timetable/faculty/{faculty_id}`            |
| Current & next class for a year   | `GET /api/timetable/year/{year_id}/current-next`     |

Full interactive docs with request/response schemas are at `/docs`.

## Conflict detection

Every `POST` / `PUT` to `/api/schedules/` runs three checks before saving:

1. **Section conflict** — the same Year already has a class in that Day+TimeSlot.
2. **Faculty conflict** — the same Faculty is already teaching a different Year in that Day+TimeSlot.
3. **Room conflict** — the same room is already booked in that Day+TimeSlot (only if a room is supplied).

If any check fails, the API responds `409 Conflict` with a clear explanation
of exactly what clashed (which schedule id, which year/faculty/room).

## Switching to PostgreSQL

Just change `DATABASE_URL` in `.env`, e.g.:

```
DATABASE_URL=postgresql://username:password@host:5432/dbname
```

`psycopg2-binary` is already in `requirements.txt`, so no extra install is needed.

## Deploying to Render / Railway

1. Push this project to a GitHub repo.
2. Create a new **Web Service** on Render (or a new project on Railway) and connect the repo.
3. Set the **Build Command**: `pip install -r requirements.txt`
4. Set the **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in the dashboard (matching `.env.example`):
   - `DATABASE_URL` — use a managed Postgres instance (Render/Railway both offer one-click Postgres)
   - `CORS_ORIGINS` — your deployed frontend's URL
   - `AUTO_SEED` — `true` for the first deploy, then optionally `false` afterward
6. Deploy. Your API will be live at the URL Render/Railway assigns, with `/docs` for interactive testing.

## Notes on the seed data

The 2nd and 3rd Year timetables share the same time-slot grid (break after
period 2, lunch after period 5). The 4th Year grid is modeled with its own
TimeSlot set since its structure differs slightly in the source image.
Faculty names, subject codes, and lab names are transcribed as closely as
possible from the uploaded image; a few small/ambiguous cells (e.g. a couple
of 3rd Year Thursday periods, some 4th Year Saturday periods left blank as
in the source) were mapped conservatively — **please review the seeded
schedule against your original document and adjust via the API or directly
in `app/database/seed.py` if any cell doesn't match your institution's copy.**
