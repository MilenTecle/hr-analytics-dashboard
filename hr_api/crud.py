from sqlalchemy.orm import Session
from . import models


# Return all employees in the database
# and filter to only return rows with complete info
def get_all_employees(db: Session):
    return db.query(models.Employee).filter(
        models.Employee.monthlyincome != None,
        models.Employee.jobrole != None,
        models.Employee.performancerating != None,
    ).all()