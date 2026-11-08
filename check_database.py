
import sqlite3
from pathlib import Path
import pandas as pd

# Locate database
BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BASE_DIR / "data" / "retail_sales.db"

# Connect to database
conn = sqlite3.connect(DATABASE_FILE)

# Read records from SQLite
df = pd.read_sql_query(
    "SELECT * FROM retail_sales",
    conn
)

print("DATABASE VERIFICATION SUCCESSFUL!")

print("\nFirst 5 records:")
print(df.head())

print("\nTotal records stored:", len(df))

print("\nTotal sales:", df["total_amount"].sum())

# Verify database table structure
print("\nDatabase Table Structure:")

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(retail_sales)")

columns = cursor.fetchall()

for column in columns:
    print(f"Column: {column[1]} | Data Type: {column[2]}")


conn.close()
