
import sqlite3

from config import load_dataset_config, get_project_path, load_config
from logger import get_logger


logger = get_logger("LOAD")


def load_data(df, dataset_name=None):

    conn = None

    try:

        logger.info("Starting database load process")

        # Load selected dataset configuration
        dataset_config = load_dataset_config(dataset_name)

        # Get database settings
        database_config = dataset_config["database"]

        database_file = get_project_path(
            database_config["file"]
        )

        table_name = database_config["table"]

        logger.info("Dataset profile: %s", dataset_name or load_config()["active_dataset"])
        logger.info("Database location: %s", database_file)
        logger.info("Target table: %s", table_name)

        # Ensure database directory exists
        database_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

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

    config = load_config()

    dataset_name = config["active_dataset"]

    from extract import extract_data
    from transform import transform_data

    raw_data = extract_data(
        dataset_name=dataset_name
    )

    transformed_data = transform_data(
        raw_data,
        dataset_name=dataset_name
    )

    load_data(
        transformed_data,
        dataset_name=dataset_name
    )
    