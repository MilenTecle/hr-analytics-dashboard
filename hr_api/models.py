from sqlalchemy import Column, Integer, String
from .database import Base

# SQLAlchemy model that maps to the "employees" table in PostgreSQL
# This defines the shape of our database table and lets us query it with Python
class Employee(Base):
    __tablename__ = "employees"

    # Use existing table in the database without modifying it
    __table_args__ = {'extend_existing': True}

    # Add composite primary key to satisfy SQLAlchemy
    age = Column(Integer, primary_key=True)
    gender = Column(String, primary_key=True)
    department = Column(String, primary_key=True)

    # Remaining fields
    attrition = Column(String)
    business_travel = Column(String)
    distance_from_home = Column(Integer)
    education = Column(Integer)
    education_field = Column(String)
    environment_satisfaction = Column(Integer)
    job_involvement = Column(Integer)
    job_level = Column(Integer)
    job_role = Column(String)
    job_satisfaction = Column(Integer)
    marital_status = Column(String)
    monthly_income = Column(Integer)
    num_companies_worked = Column(Integer)
    over_time = Column(String)
    percent_salary_hike = Column(Integer)
    performance_rating = Column(Integer)
    relationship_satisfaction = Column(Integer)
    stock_option_level = Column(Integer)
    total_working_years = Column(Integer)
    training_times_last_year = Column(Integer)
    work_life_balance = Column(Integer)
    years_at_company = Column(Integer)
    years_in_current_role = Column(Integer)
    years_since_last_promotion = Column(Integer)
    years_with_curr_manager = Column(Integer)