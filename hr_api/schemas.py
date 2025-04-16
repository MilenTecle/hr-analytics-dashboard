from pydantic import BaseModel
from typing import Optional

# Schema used for reading employee data from the database
class EmployeeBase(BaseModel):
    age: int
    attrition: str
    business_travel: Optional[str]
    department: str
    distance_from_home: Optional[int]  
    education: int
    education_field: Optional[str]
    environment_satisfaction: Optional[int]
    gender: str
    job_involvement: Optional[int]
    job_level: Optional[int]
    job_role: Optional[str]
    job_satisfaction: Optional[int]
    marital_status: Optional[str]
    monthly_income: Optional[int]
    num_companies_worked: Optional[int]
    over_time: Optional[str]
    percent_salary_hike: Optional[int]
    performance_rating: Optional[int]
    relationship_satisfaction: Optional[int]
    stock_option_level: Optional[int]
    total_working_years: Optional[int]
    training_times_last_year: Optional[int]
    work_life_balance: Optional[int]
    years_at_company: Optional[int]
    years_in_current_role: Optional[int]
    years_since_last_promotion: Optional[int]
    years_with_curr_manager: Optional[int]

    class Config:
        from_attributes = True  # /Pydantic v2 version of orm_mode