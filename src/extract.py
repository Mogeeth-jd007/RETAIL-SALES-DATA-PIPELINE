
import pandas as pd
from pathlib import Path

from config import load_config
from logger import get_logger


logger = get_logger("EXTRACT")


def extract_data(filename=None):

    try:

        # Load project configuration
        config = load_config()

        # Locate the project directory
        project_dir = Path(__file__).resolve().parent.parent

        # Get filename from configuration
        if filename is None:
            filename = config["input_file"]

        # Get raw data directory from configuration
        raw_directory = project_dir / config["directories"]["raw"]

        # Locate the CSV file
        file_path = raw_directory / filename

        logger.info("Starting extraction from: %s", filename)

        # Check whether the file exists
        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        # Read CSV data
        df = pd.read_csv(file_path)

        logger.info("Data extracted successfully")
        logger.info("Total records extracted: %s", len(df))

        return df

    except Exception:
        logger.exception("Data extraction failed")
        raise


if __name__ == "__main__":

    sales_data = extract_data()

    print("\nFirst 5 records:")
    print(sales_data.head())

    print("\nTotal records:", len(sales_data))
