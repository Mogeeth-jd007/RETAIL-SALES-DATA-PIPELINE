
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / "data" / "retail_sales.db"

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# Count total records
cursor.execute("SELECT COUNT(*) FROM retail_sales")
total_records = cursor.fetchone()[0]

print("DATABASE VERIFICATION")
print("---------------------")
print(f"Total records: {total_records}")

# Display first 5 records
cursor.execute("SELECT * FROM retail_sales LIMIT 5")

for row in cursor.fetchall():
    print(row)

conn.close()
