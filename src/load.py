
import sqlite3

from config import load_config, get_project_path
from logger import get_logger


logger = get_logger("LOAD")


def load_data(df):

    conn = None

    try:

        logger.info("Starting database load process")

        # Load configuration
        config = load_config()

        # Get database settings
        database_file = get_project_path(config["database"]["file"])
        table_name = config["database"]["table"]

        logger.info("Database location: %s", database_file)
        logger.info("Target table: %s", table_name)

        # Connect to SQLite database
        conn = sqlite3.connect(database_file)

        logger.info("Database connection established")

        # Load data into database
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists="replace",
            index=False
        )

        logger.info("Data successfully loaded into SQLite database")
        logger.info("Total records loaded: %s", len(df))
        logger.info("Target table: %s", table_name)

    except Exception:
        logger.exception("Database loading failed")
        raise

    finally:

        if conn is not None:
            conn.close()
            logger.info("Database connection closed")


if __name__ == "__main__":

    from extract import extract_data
    from transform import transform_data

    sales_data = extract_data()
    transformed_data = transform_data(sales_data)

    load_data(transformed_data)
