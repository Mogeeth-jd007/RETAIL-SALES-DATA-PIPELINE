
import sqlite3

from config import load_config, get_project_path


def load_data(df):

    print("\nStarting Load Process...")

    # Load configuration
    config = load_config()

    # Get database settings
    database_file = get_project_path(config["database"]["file"])
    table_name = config["database"]["table"]

    # Connect to SQLite database
    conn = sqlite3.connect(database_file)

    try:

        # Load data into database
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists="replace",
            index=False
        )

    finally:
        conn.close()

    print("\nData successfully loaded into SQLite database!")
    print(f"Total records loaded: {len(df)}")
    print(f"Database location: {database_file}")
    print(f"Table name: {table_name}")
