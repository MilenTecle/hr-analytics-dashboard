import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_URL
import pandas as pd
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

# Use local full dataset only if running manually
IS_LOCAL = os.getenv("RUN_LOCAL", "false").lower() == "true"

if IS_LOCAL:
    CSV_PATH = "data/cleaned_hr_data_final.csv"
else:
    CSV_PATH = "data/cleaned_hr_data_final.example.csv"

# Target table in the PostgreSQL database
TABLE_NAME = "employees"


def connect():
    """"
    Establish a connection to the PostgreSQL database using credentials
    parsed from the DATABASE_URL in the .env file.
    """
    result = urlparse(DATABASE_URL)
    return psycopg2.connect(
        dbname=result.path[1:],  # Strip leading slash from /dbname
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port,
        sslmode='require'
    )


def load_csv():
    """
    Load the cleaned HR data from CSV, normalize column names,
    and ensure required fields exist. Falls back to example CSV if real one is missing.
    """
    if not os.path.exists(CSV_PATH):
        print(f"{CSV_PATH} not found. Falling back to example CSV.")
        fallback_path = "data/cleaned_hr_data_final.example.csv"
        if not os.path.exists(fallback_path):
            raise FileNotFoundError("Neither real nor fallback CSV found.")
        use_path = fallback_path
    else:
        use_path = CSV_PATH

    df = pd.read_csv(use_path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Rename expected columns if needed
    df.rename(columns={
        "job_role": "jobrole"
    }, inplace=True)

    # Add a synthetic employee_id if missing
    if "employee_id" not in df.columns:
        df.insert(0, "employee_id", range(1, len(df) + 1))

    expected_columns = ["employee_id", "age", "gender",
                        "jobrole", "attrition", "monthlyincome"]
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    return df


def refresh_table(df):
    """
    Replace all records in the 'employees' table with the latest data from the CSV.
    This uses a truncate-and-replace strategy.
    """
    conn = connect()
    cursor = conn.cursor()

    print("Truncating table...")
    cursor.execute(f"TRUNCATE TABLE {TABLE_NAME}")

    print("Inserting new records...")
    for _, row in df.iterrows():
        try:
            values = [row.get(col, None) for col in [
                'employee_id', 'age', 'gender', 'department', 'attrition',
                'businesstravel', 'dailyrate', 'distancefromhome', 'education',
                'educationfield', 'environmentsatisfaction', 'hourlyrate',
                'jobinvolvement', 'joblevel', 'jobrole', 'jobsatisfaction',
                'maritalstatus', 'monthlyincome', 'monthlyrate',
                'numcompaniesworked', 'overtime', 'percentsalaryhike',
                'performancerating', 'relationshipsatisfaction',
                'stockoptionlevel', 'totalworkingyears',
                'trainingtimeslastyear', 'worklifebalance',
                'yearsatcompany', 'yearsincurrentrole',
                'yearssincelastpromotion', 'yearswithcurrmanager'
            ]]
            cursor.execute(
                f"""
                INSERT INTO {TABLE_NAME} (
                    employee_id, age, gender, department, attrition,
                    businesstravel, dailyrate, distancefromhome, education,
                    educationfield, environmentsatisfaction, hourlyrate,
                    jobinvolvement, joblevel, jobrole, jobsatisfaction,
                    maritalstatus, monthlyincome, monthlyrate,
                    numcompaniesworked, overtime, percentsalaryhike,
                    performancerating, relationshipsatisfaction,
                    stockoptionlevel, totalworkingyears,
                    trainingtimeslastyear, worklifebalance,
                    yearsatcompany, yearsincurrentrole,
                    yearssincelastpromotion, yearswithcurrmanager
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                values
            )
        except Exception as e:
            print(f"Error inserting row: {e}")
            continue

    conn.commit()
    cursor.close()
    conn.close()
    print(f"ETL complete: {len(df)} records inserted into '{TABLE_NAME}'.")


def main():
    """
    Main entry point for the ETL script.
    Loads data, connects to the database, and refreshes the target table.
    """
    print("Starting ETL job...")
    df = load_csv()
    refresh_table(df)


# Execute the script
if __name__ == "__main__":
    main()
