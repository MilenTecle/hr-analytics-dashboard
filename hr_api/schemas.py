from pydantic import BaseModel

# Schema used for reading employee data from the database
class EmployeeBase(BaseModel):
    age: int
    attrition: str
    business_travel: str
    department: str
    distance_from_home: int
    education: int
    education_field: str
    environment_satisfaction: int
    gender: str
    job_involvement: int
    job_level: int
    job_role: str
    job_satisfaction: int
    marital_status: str
    monthly_income: int
    num_companies_worked: int
    over_time: str
    percent_salary_hike: int
    performance_rating: int
    relationship_satisfaction: int
    stock_option_level: int
    total_working_years: int
    training_times_last_year: int
    work_life_balance: int
    years_at_company: int
    years_in_current_role: int
    years_since_last_promotion: int
    years_with_curr_manager: int

    model_config = {
      "from_attributes": True  # Enables compatibility with SQLAlchemy models
    }