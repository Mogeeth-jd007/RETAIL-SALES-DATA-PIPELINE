
import pandas as pd
from pathlib import Path
from config import load_config


def extract_data(filename=None):

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

    # Check whether the file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    # Read CSV data
    df = pd.read_csv(file_path)

    print("Data extracted successfully!")
    print("Source file:", filename)

    return df


if __name__ == "__main__":

    sales_data = extract_data()

    print("\nFirst 5 records:")
    print(sales_data.head())

    print("\nTotal records:", len(sales_data))
