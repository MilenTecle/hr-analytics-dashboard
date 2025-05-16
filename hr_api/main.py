from typing import Optional
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from . import schemas, crud
from .database import SessionLocal, get_db
from .refresh import router as refresh_router

app = FastAPI(title="HR Dashboard API")
app.include_router(refresh_router)


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


# GET /employees - return paginated list of employees with optional filters
# Supports skip & limit query parameters for pagination
@app.get("/employees", response_model=list[schemas.EmployeeBase])
def read_employees(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, le=1000), 
    db: Session = Depends(get_db)
):
    return crud.get_all_employees(db, skip=skip, limit=limit)


# GET /kpi-summary - return key HR metrics for dashboard (headcount, avg age, avg tenure)
@app.get("/kpi-summary", response_model=schemas.KPISummary)
def read_kpi_summary(db: Session = Depends(get_db)):
    return crud.get_kpi_summary(db)


# GET /departments - return department-wise headcount and average income
@app.get("/departments", response_model=list[schemas.DepartmentSummary])
def read_departments_summary(db: Session = Depends(get_db)):
    return crud.get_departments_summary(db)


# GET /attrition-rate - return overall or filtered attrition rate
@app.get("/attrition-rate", response_model=schemas.AttritionRateResponse)
def get_attrition_rate(
    gender: Optional[str] = Query(None, pattern="^(Male|Female)$"),
    department: Optional[str] = Query(None, min_length=2),
    db: Session = Depends(get_db),
):
    return crud.get_attrition_rate(db, gender=gender, department=department)