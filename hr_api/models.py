from sqlalchemy import Column, Integer, String
from .database import Base

# SQLAlchemy model that maps to the "employees" table in PostgreSQL
class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {'extend_existing': True}

    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Fields
    age = Column(Integer)
    gender = Column(String(10))
    department = Column(String(50))
    attrition = Column(String(50))
    businesstravel = Column(String(50))
    dailyrate = Column(Integer)
    distancefromhome = Column(Integer)
    education = Column(Integer)
    educationfield = Column(String(50))
    environmentsatisfaction = Column(Integer)
    hourlyrate = Column(Integer)
    jobinvolvement = Column(Integer)
    joblevel = Column(Integer)
    jobrole = Column(String(50))
    jobsatisfaction = Column(Integer)
    maritalstatus = Column(String(50))
    monthlyincome = Column(Integer)
    monthlyrate = Column(Integer)
    numcompaniesworked = Column(Integer)
    overtime = Column(String(10))
    percentsalaryhike = Column(Integer)
    performancerating = Column(Integer)
    relationshipsatisfaction = Column(Integer)
    stockoptionlevel = Column(Integer)
    totalworkingyears = Column(Integer)
    trainingtimeslastyear = Column(Integer)
    worklifebalance = Column(Integer)
    yearsatcompany = Column(Integer)
    yearsincurrentrole = Column(Integer)
    yearssincelastpromotion = Column(Integer)
    yearswithcurrmanager = Column(Integer)