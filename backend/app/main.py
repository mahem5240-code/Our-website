"""
College AIML Timetable Management System — FastAPI application entry point.

Run locally with:
    uvicorn app.main:app --reload

Swagger UI:  http://127.0.0.1:8000/docs
ReDoc:       http://127.0.0.1:8000/redoc
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database.db import Base, engine, SessionLocal
from app.database.seed import seed_if_empty
from app.routers import years, faculty, subjects, time_slots, class_schedules, timetable_views

# Create all tables if they don't already exist.
# (For a real production project you would use Alembic migrations instead —
# alembic is included in requirements.txt and ready to be initialized.)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="College AIML Timetable Management System",
    description=(
        "REST API for managing the AIML department's 2nd, 3rd and 4th Year "
        "timetables — subjects, labs, faculty, breaks, lunch, and full "
        "weekly/day/subject/faculty views, with built-in conflict detection."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS — allows a frontend (React, Vue, etc.) running on a different origin
# to call this API. Configure allowed origins via CORS_ORIGINS in .env.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Global error handling — turns unexpected exceptions into clean JSON
# instead of leaking a stack trace to the client.
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


# ---------------------------------------------------------------------------
# Startup: seed the database with sample data (from the uploaded timetable)
# if it's empty. Controlled by AUTO_SEED in .env.
# ---------------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    if settings.AUTO_SEED:
        db = SessionLocal()
        try:
            seed_if_empty(db)
        finally:
            db.close()


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(years.router)
app.include_router(faculty.router)
app.include_router(subjects.router)
app.include_router(time_slots.router)
app.include_router(class_schedules.router)
app.include_router(timetable_views.router)


@app.get("/", tags=["Health"])
def root():
    """Simple health check / welcome endpoint."""
    return {
        "message": "College AIML Timetable Management System API is running.",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
