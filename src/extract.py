import pandas as pd
from pathlib import Path

from config import load_config, load_dataset_config
from logger import get_logger

logger = get_logger("EXTRACT")


def extract_data(filename=None, dataset_name=None):

    try:

        # Load complete project configuration
        config = load_config()

        # Load selected dataset configuration
        dataset_config = load_dataset_config(dataset_name)

        # Locate project directory
        project_dir = Path(__file__).resolve().parent.parent

        # Use configured filename if none is provided
        if filename is None:
            filename = dataset_config["input_file"]

        # Locate raw data directory
        raw_directory = project_dir / config["directories"]["raw"]

        # Locate CSV file
        file_path = raw_directory / filename

        logger.info("Starting extraction")
        logger.info("Dataset profile: %s", dataset_name or config["active_dataset"])
        logger.info("Input file: %s", filename)

        # Check whether file exists
        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        # Read CSV
        df = pd.read_csv(file_path)

        logger.info("Data extracted successfully")
        logger.info("Total records extracted: %s", len(df))

        return df

    except Exception:
        logger.exception("Data extraction failed")
        raise