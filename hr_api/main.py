from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import schemas, crud
from .database import SessionLocal

app = FastAPI(title="HR Dashboard API")


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the HR Dashboard API"}


# GET /employees - return all employees
@app.get("/employees", response_model=list[schemas.EmployeeBase])
def read_employees(db: Session = Depends(get_db)):
    print("/employees was reached")
    return crud.get_all_employees(db)


# GET /kpi-summary - return key HR metrics for dashboard (headcount, avg age, avg tenure)
@app.get("/kpi-summary", response_model=schemas.KPISummary)
def read_kpi_summary(db: Session = Depends(get_db)):
    return crud.get_kpi_summary(db)