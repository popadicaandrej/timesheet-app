"""
FastAPI Timesheet Backend
Intended for deployment on Render.
DATABASE_URL must be set in environment variables.
"""
import csv
from io import StringIO
from datetime import date

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import get_db
from models import User, Timesheet as TimesheetModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----- Pydantic schemas -----

class UserOut(BaseModel):
    id: int
    name: str
    phone_number: str | None

    class Config:
        from_attributes = True


class TimesheetCreate(BaseModel):
    user_id: int
    date: str
    hours: float
    project: str
    description: str


class TimesheetOut(BaseModel):
    id: int
    user_id: int | None
    date: date
    hours: float
    project: str
    description: str

    class Config:
        from_attributes = True


# ----- Endpoints -----

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    """List all users (for dropdowns and export filter)."""
    users = db.query(User).order_by(User.name).all()
    return users


@app.post("/timesheet")
def create_timesheet(entry: TimesheetCreate, db: Session = Depends(get_db)):
    try:
        # Parse date string (YYYY-MM-DD) to date for the DB
        entry_date = date.fromisoformat(entry.date) if isinstance(entry.date, str) else entry.date
        db_entry = TimesheetModel(
            user_id=entry.user_id,
            date=entry_date,
            hours=entry.hours,
            project=entry.project,
            description=entry.description,
        )
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return {"message": "Timesheet saved successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/export")
def export_csv(
    user_id: int = Query(..., description="Filter by user id"),
    db: Session = Depends(get_db),
):
    """Export timesheets for one user as CSV (with user name in header)."""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        rows = (
            db.query(TimesheetModel)
            .filter(TimesheetModel.user_id == user_id)
            .order_by(TimesheetModel.date.desc(), TimesheetModel.id.desc())
            .all()
        )

        output = StringIO()
        writer = csv.writer(output, delimiter=";")
        writer.writerow(["user_name", "date", "hours", "project", "description"])
        for r in rows:
            writer.writerow([user.name, r.date, r.hours, r.project, r.description])

        csv_content = output.getvalue()
        csv_content = "\ufeff" + csv_content

        return Response(
            content=csv_content,
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": 'attachment; filename="timesheets.csv"'},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
