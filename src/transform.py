
import pandas as pd
import re
from pathlib import Path

from extract import extract_data
from config import load_config
from logger import get_logger


logger = get_logger("TRANSFORM")


def standardize_column_names(df):

    df = df.copy()

    standardized_columns = []

    for column in df.columns:

        column = column.strip().lower()

        column = re.sub(r"[\s\-]+", "_", column)

        column = re.sub(r"[^a-z0-9_]", "", column)

        column = re.sub(r"_+", "_", column)

        column = column.strip("_")

        standardized_columns.append(column)

    df.columns = standardized_columns

    return df

def clean_text_columns(df):

    df = df.copy()

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

        df[column] = df[column].replace("", pd.NA)

        logger.info(
            "Text column cleaned: %s",
            column
        )

    return df

def detect_data_types(df):

    df = df.copy()

    for column in df.columns:

        # Skip identifier columns
        if column.endswith("_id"):
            continue

        # Skip columns that are already datetime
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            continue

        # Attempt numeric conversion
        converted_column = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        # Calculate the percentage of successfully converted values
        total_values = df[column].notna().sum()

        if total_values == 0:
            continue

        numeric_values = converted_column.notna().sum()

        numeric_ratio = numeric_values / total_values

        # Convert only if at least 80% of values are numeric
        if numeric_ratio >= 0.80:

            df[column] = converted_column

            logger.info(
                "Numeric data type detected for column: %s (%.0f%%)",
                column,
                numeric_ratio * 100
            )

    return df


def transform_data(df):

    try:

        logger.info("Starting data transformation")

        # Work on a copy of the original data
        df = df.copy()

        # 1. Standardize column names
        df = standardize_column_names(df)

        logger.info("Column names standardized")

        # 2. Clean text columns
        df = clean_text_columns(df)

        logger.info("Text columns cleaned")



        # 3. Convert configured date columns
        config = load_config()
        rules = config["transformation"]

        for column in rules["date_columns"]:

            if column not in df.columns:
                raise ValueError(
                    f"Configured date column missing: {column}"
                )

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            logger.info(
                "Date conversion completed for column: %s",
                column
            )

        # 4. Automatically detect numeric columns
        df = detect_data_types(df)

        logger.info("Data type detection completed successfully")

        # 5. Calculate total sales using configuration
        if rules["calculate_total"]:

            quantity_column = rules["quantity_column"]
            price_column = rules["price_column"]
            total_column = rules["total_column"]

            required_columns = [
                quantity_column,
                price_column
            ]

            for column in required_columns:
                if column not in df.columns:
                    raise ValueError(
                        f"Required column for total calculation missing: {column}"
                    )

            df[total_column] = (
                df[quantity_column] * df[price_column]
            )

            logger.info(
                "Total sales calculated using %s and %s",
                quantity_column,
                price_column
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
