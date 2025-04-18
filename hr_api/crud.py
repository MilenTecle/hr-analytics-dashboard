from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models


# Return paginated list of employees in the database
# and filter to only return rows with complete info
def get_all_employees(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Employee)
        .filter(
            models.Employee.monthlyincome != None,
            models.Employee.jobrole != None,
            models.Employee.performancerating != None,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


# Return summary KPIs for the HR dashboard
# Includes total headcount, average age, and average tenure
def get_kpi_summary(db: Session):
    total_employees = db.query(func.count()).select_from(models.Employee).scalar()
    avg_age = db.query(func.avg(models.Employee.age)).scalar()
    avg_tenure = db.query(func.avg(models.Employee.yearsatcompany)).scalar()

    return {
        "headcount": total_employees,
        "avg_age": round(avg_age, 1) if avg_age else None,
        "avg_tenure": round(avg_tenure, 1) if avg_tenure else None
    }


# Return department-level summary statistics for the HR dashboard
def get_departments_summary(db):
    results = (
        db.query(
            models.Employee.department.label("department"),
            func.count().label("headcount"),
            func.avg(models.Employee.monthlyincome).label("avg_income")
        )
        .group_by(models.Employee.department)
        .all()
    )

    # Convert results into list of dictionaries
    return [
        {
            "department": dept,
            "headcount": count,
            "avg_income": round(avg_income, 2) if avg_income else None
        }
        for dept, count, avg_income in results
    ]


# Return attrition rate (percentage of employees who left)
def get_attrition_rate(db: Session, gender: str = None, department: str = None):
    query = db.query(models.Employee)

    # Optional filters
    if gender:
        query = query.filter(models.Employee.gender == gender)
    if department:
        query = query.filter(models.Employee.department == department)

    total = query.count()
    attritions = query.filter(models.Employee.attrition == "Yes").count()

    if total == 0:
        return {"attrition_rate": None}  # avoid division by zero

    rate = round((attritions / total) * 100, 2)
    return {"attrition_rate": rate}