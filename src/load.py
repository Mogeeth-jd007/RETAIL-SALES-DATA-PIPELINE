
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / "data" / "retail_sales.db"


def load_data(df):

    print("Starting Load Process...")

    conn = sqlite3.connect(DATABASE_FILE)

    df.to_sql(
        name="retail_sales",
        con=conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Data successfully loaded into SQLite database!")
    print(f"Total records loaded: {len(df)}")
    print(f"Database location: {DATABASE_FILE}")
