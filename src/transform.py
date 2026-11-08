import pandas as pd
from pathlib import Path

from extract import extract_data
from config import load_config
from logger import get_logger


logger = get_logger("TRANSFORM")


def transform_data(df):

    try:

        logger.info("Starting data transformation")

        # Work on a copy of the original data
        df = df.copy()

        # 1. Clean column names
        df.columns = df.columns.str.strip().str.lower()

        logger.info("Column names cleaned")

        # 2. Clean text columns
        for column in ["customer_name", "product", "category", "city"]:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

        # Convert empty strings into missing values
        for column in ["customer_name", "product", "category", "city"]:

            df[column] = df[column].replace("", pd.NA)

        logger.info("Text columns cleaned")

        # 3. Convert data types
        df["order_date"] = pd.to_datetime(
            df["order_date"], errors="coerce"
        )

        df["quantity"] = pd.to_numeric(
            df["quantity"], errors="coerce"
        )

        df["price"] = pd.to_numeric(
            df["price"], errors="coerce"
        )

        logger.info("Data types converted successfully")

        # 4. Calculate total sales
        df["total_amount"] = df["quantity"] * df["price"]

        logger.info("Total sales calculated")

        logger.info(
            "Transformation completed. Records preserved: %s",
            len(df)
        )

        return df

    except Exception:
        logger.exception("Data transformation failed")
        raise


if __name__ == "__main__":

    # Load configuration
    config = load_config()

    # Extract raw data
    sales_data = extract_data()

    # Transform raw data
    cleaned_data = transform_data(sales_data)

    # Locate project directory
    project_dir = Path(__file__).resolve().parent.parent

    # Get processed directory from configuration
    output_dir = project_dir / config["directories"]["processed"]
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get output filename from configuration
    output_file = output_dir / config["processed_file"]

    # Save transformed data
    cleaned_data.to_csv(output_file, index=False)

    print("\nTransformed data:")
    print(cleaned_data)

    print("\nTotal records:", len(cleaned_data))
    print("\nTotal sales:", cleaned_data["total_amount"].sum())

    print("\nProcessed file saved at:", output_file)