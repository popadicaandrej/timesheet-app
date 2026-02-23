"""
FastAPI Timesheet Backend
Intended for deployment on Render.
DATABASE_URL must be set in environment variables.
"""
import os
import csv
import psycopg2
from io import StringIO
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

class Timesheet(BaseModel):
    name: str
    date: str
    hours: float
    project: str
    description: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/timesheet")
def create_timesheet(entry: Timesheet):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO timesheets (name, date, hours, project, description)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (entry.name, entry.date, entry.hours, entry.project, entry.description)
        )

        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Timesheet saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export")
def export_csv(name: str = Query(..., description="Filter by employee name")):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT name, date, hours, project, description
            FROM timesheets
            WHERE name = %s
            ORDER BY date DESC, id DESC
            """,
            (name,)
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        output = StringIO()
        writer = csv.writer(output, delimiter=";")
        writer.writerow(["name", "date", "hours", "project", "description"])
        for r in rows:
            writer.writerow(r)

        csv_content = output.getvalue()
        csv_content = "\ufeff" + csv_content

        return Response(
            content=csv_content,
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": 'attachment; filename="timesheets.csv"'}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

