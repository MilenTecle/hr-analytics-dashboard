from pydantic import BaseModel, Field


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