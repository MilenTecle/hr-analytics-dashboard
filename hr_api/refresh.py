import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import Employee
from .database import get_db

# Create a new API router to register custom endpoints
router = APIRouter()

@router.post("/refresh-employees")
def refresh_employees(db: Session = Depends(get_db)):
    """
    Refreshes the employee ata in the database by:
    - Loading the latest cleaned CSV
    - Normalizing column names
    - Deleting existing records
    - Inserting updated employee records
    """
    try:
        # Load the cleaned HR data from CSV
        df = pd.read_csv("cleaned_hr_data_final.csv")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Rename expeced columns to match the database model
        df.rename(columns={"job_role": "jobrole"}, inplace=True)

        # Generate default employee_id if it's missing
        if "employee_id" not in df.columns:
            df.insert(0, "employee_id", range(1, len(df) + 1))

            db.query(Employee).delete()

            # Insert each row into the database as an Employee object
            for _, row in df.iterrows():
                emp = Employee(
                    employee_id=row["emplyee_id"],
                    age=row["age"],
                    gender=row["gender"],
                    jobrole=row["jobrole"],
                    attrition=row["attrition"],
                    monthlyincome=row["monthlyincome"]
                )
                db.add(emp)

            # Commit all changes to the database
            db.commit()
            return {"status": "success", "records_inserted": len(df)}
        
    except Exception as e:
        # Roll back any changes on error and return HTTP 500
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))