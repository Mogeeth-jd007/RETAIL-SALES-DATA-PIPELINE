
import pandas as pd
from pathlib import Path


def extract_data(filename="retail_sales.csv"):

    # Locate the project directory
    project_dir = Path(__file__).resolve().parent.parent

    # Locate the raw CSV file
    file_path = project_dir / "data" / "raw" / filename

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
