from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models


# Return all employees in the database
# and filter to only return rows with complete info
def get_all_employees(db: Session):
    return db.query(models.Employee).filter(
        models.Employee.monthlyincome != None,
        models.Employee.jobrole != None,
        models.Employee.performancerating != None,
    ).all()


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