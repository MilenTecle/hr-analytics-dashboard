import pandas as pd
import psycopg2
from urllib.parse import urlparse
from config import DATABASE_URL

# Path to the cleaned HR data CSV file
CSV_PATH = "./cleaned_hr_data_final.csv"

# Target table in the PostgreSQL database
TABLE_NAME = "employees"

def connect():
    """"
    Establish a connection to the PostgreSQL database using credentials
    parsed from the DATABASE_URL in the .env file.
    """
    result = urlparse(DATABASE_URL)
    return psycopg2.connect(
        dbname=result.path[1:], # Strip leading slash from /dbname
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

def load_csv():
    """
    Load the cleaned HR data from CSV, normalize column names,
    and ensure requried fields exist.
    """
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")   # Removes leading/traling spaces and convert column names to lowercase

    # Rename expected columns if needed
    df.rename(columns={
        "job_role": "jobrole"
    }, inplace=True)

    # Add a synthetic employee_id if missing
    if "employee_id" not in df.columns:
        df.insert(0, "employee_id", range(1, len(df) + 1))

    expected_columns = ["employee_id", "age", "gender", "jobrole", "attrition", "monthlyincome"]
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    return df

def refresh_table(df):
    """
    Replace all records in the 'employees' table with the latest data from the CSV.
    This uses a truncate-and-replace strategy for simplicity.
    """
    conn = connect()
    cursor = conn.cursor()

    print("Truncating table...")
    cursor.execute(f"TRUNCATE TABLE {TABLE_NAME}")  # Clears all existing data

    print("Instering new records...")
    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT INTO {TABLE_NAME} (employee_id, age, gender, jobrole, attrition, monthlyincome)
            VALUES (%s, %s, %s), %s, %s, %s)
            """, (
                int(row["employee_id"]),
                int(row["age"]),
                row["gender"],
                row["jobrole"],
                row["attrition"],
                int(row["monthlyincome"])
            ))
        
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