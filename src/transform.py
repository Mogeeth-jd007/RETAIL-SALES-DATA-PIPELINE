
import pandas as pd
import re
from pathlib import Path

from extract import extract_data
from config import load_config, load_dataset_config
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

        logger.info("Text column cleaned: %s", column)

    return df


def detect_data_types(df):

    df = df.copy()

    for column in df.columns:

        if column.endswith("_id"):
            continue

        if pd.api.types.is_datetime64_any_dtype(df[column]):
            continue

        converted_column = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        total_values = df[column].notna().sum()

        if total_values == 0:
            continue

        numeric_values = converted_column.notna().sum()
        numeric_ratio = numeric_values / total_values

        if numeric_ratio >= 0.80:

            df[column] = converted_column

            logger.info(
                "Numeric data type detected for column: %s (%.0f%%)",
                column,
                numeric_ratio * 100
            )

    return df


def transform_data(df, dataset_name=None):

    try:

        logger.info("Starting data transformation")

        # Work on a copy
        df = df.copy()

        # 1. Standardize column names
        df = standardize_column_names(df)

        logger.info("Column names standardized")

        # 2. Clean text columns
        df = clean_text_columns(df)

        logger.info("Text columns cleaned")

        # 3. Load selected dataset transformation rules
        dataset_config = load_dataset_config(dataset_name)
        rules = dataset_config["transformation"]

        # 4. Convert configured date columns
        for column in rules.get("date_columns", []):

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

        # 5. Detect numeric columns
        df = detect_data_types(df)

        logger.info("Data type detection completed successfully")

        # 6. Calculate total only when enabled
        if rules.get("calculate_total", False):

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
                "Total calculated using %s and %s",
                quantity_column,
                price_column
            )

        return df

    except Exception:
        logger.exception("Data transformation failed")
        raise


if __name__ == "__main__":

    config = load_config()

    dataset_name = config["active_dataset"]

    dataset_config = load_dataset_config(dataset_name)

    raw_data = extract_data(dataset_name=dataset_name)

    cleaned_data = transform_data(
        raw_data,
        dataset_name=dataset_name
    )

    project_dir = Path(__file__).resolve().parent.parent

    output_dir = project_dir / config["directories"]["processed"]
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / (
        dataset_name + "_cleaned.csv"
    )

    cleaned_data.to_csv(output_file, index=False)

    print("\nTransformed data:")
    print(cleaned_data)

    print("\nTotal records:", len(cleaned_data))

    if "total_amount" in cleaned_data.columns:
        print(
            "\nTotal sales:",
            cleaned_data["total_amount"].sum()
        )

    print("\nProcessed file saved at:", output_file)
