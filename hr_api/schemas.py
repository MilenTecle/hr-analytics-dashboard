from pydantic import BaseModel, Field


# Pydantic schema used for serializing employee data returned by the API
# Matches the structure of the Employee model and supports JSON response formatting
class EmployeeBase(BaseModel):
    age: int
    gender: str
    department: str
    attrition: str
    businesstravel: str
    dailyrate: int
    distancefromhome: int
    education: int
    educationfield: str
    environmentsatisfaction: int
    hourlyrate: int
    jobinvolvement: int
    joblevel: int
    jobrole: str
    jobsatisfaction: int
    maritalstatus: str
    monthlyincome: int
    monthlyrate: int
    numcompaniesworked: int
    overtime: str
    percentsalaryhike: int
    performancerating: int
    relationshipsatisfaction: int
    stockoptionlevel: int
    totalworkingyears: int
    trainingtimeslastyear: int
    
    # Fix aliases for snake_case expectations
    years_at_company: int = Field(alias="yearsatcompany")
    years_in_current_role: int = Field(alias="yearsincurrentrole")
    years_since_last_promotion: int = Field(alias="yearssincelastpromotion")
    years_with_curr_manager: int = Field(alias="yearswithcurrmanager")

    class Config:
        from_attributes = True  # Pydantic v2+


# Pydantic schema for KPI summary response
class KPISummary(BaseModel):
    headcount: int
    avg_age: float | None
    avg_tenure: float | None


# Pydantic schema for department summary response
class DepartmentSummary(BaseModel):
    department: str
    headcount: int
    avg_income: float | None


# Pydantic schema for attrition rate response
class AttritionRate(BaseModel):
    attrition_rate: float | None