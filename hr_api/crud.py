from sqlalchemy.orm import Session
from . import models

# Return all employees in the database
def get_all_employees(db: Session):
    return db.query(models.Employee).all()