import pandas as pd

# Load the dataset
df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")

# Drop unnecessary columns
df.drop(columns=["EmployeeCount", "Over18", "StandardHours", "EmployeeNumber"], inplace=True)

# Normalize text
df['Attrition'] = df['Attrition'].str.strip().str.capitalize()
df['Department'] = df['Department'].str.title()

# Rename columns to snake_case
df.columns = [col.lower().replace(" ", "_").replace("-", "_") for col in df.columns]

# Save the cleaned file
df.to_csv("cleaned_hr_data.csv", index=False)

print("Cleaned data saved as cleaned_hr_data.csv")