
import pandas as pd
from pathlib import Path

from extract import extract_data
from config import load_config
from logger import get_logger


logger = get_logger("VALIDATE")


def validate_data(df):

    try:

        logger.info("========== DATA QUALITY REPORT ==========")

        total_records = len(df)

        logger.info("Total records: %s", total_records)

        # 1. Check missing values
        logger.info("1. MISSING VALUES")

        for column in df.columns:
            missing = df[column].isna().sum()
            logger.info("%s: %s missing values", column, missing)

        # 2. Check duplicate orders
        duplicates = df["order_id"].duplicated().sum()

        logger.info("Duplicate orders: %s", duplicates)

        # 3. Check invalid dates
        dates = pd.to_datetime(
            df["order_date"], errors="coerce"
        )

        logger.info("Invalid dates: %s", dates.isna().sum())

        # 4. Check invalid numeric values
        for column in ["quantity", "price"]:

            values = pd.to_numeric(
                df[column], errors="coerce"
            )

            invalid = (
                values.isna() & df[column].notna()
            ).sum()

            logger.info("Invalid %s values: %s", column, invalid)

        # 5. Check negative or zero values
        for column in ["quantity", "price"]:

            values = pd.to_numeric(
                df[column], errors="coerce"
            )

            non_positive = (
                (values <= 0) & values.notna()
            ).sum()

            logger.info(
                "Non-positive %s values: %s",
                column,
                non_positive
            )

        logger.info("Data quality validation completed")

    except Exception:
        logger.exception("Data quality validation failed")
        raise


def classify_records(df):

    try:

        logger.info("Starting record classification")

        df = df.copy()

        # 1. Convert columns to appropriate formats
        df["order_date"] = pd.to_datetime(
            df["order_date"], errors="coerce"
        )

        df["quantity"] = pd.to_numeric(
            df["quantity"], errors="coerce"
        )

        df["price"] = pd.to_numeric(
            df["price"], errors="coerce"
        )

        # 2. Identify duplicate order IDs
        duplicate_orders = (
            df["order_id"].notna()
            & df["order_id"].duplicated(keep="first")
        )

        # 3. Identify critical errors
        critical_errors = (
            df["order_id"].isna()
            | df["order_date"].isna()
            | df["quantity"].isna()
            | df["price"].isna()
            | (df["quantity"] <= 0)
            | (df["price"] <= 0)
            | duplicate_orders
        )

        # 4. Identify non-critical errors
        warnings = (
            df["customer_name"].isna()
            | df["product"].isna()
            | df["category"].isna()
            | df["city"].isna()
        )

        # 5. Assign classification
        df["status"] = "VALID"

        df.loc[warnings & ~critical_errors, "status"] = "WARNING"

        df.loc[critical_errors, "status"] = "REJECTED"

        # 6. Generate classification summary
        valid_count = (df["status"] == "VALID").sum()
        warning_count = (df["status"] == "WARNING").sum()
        rejected_count = (df["status"] == "REJECTED").sum()

        logger.info("Valid records: %s", valid_count)
        logger.info("Warning records: %s", warning_count)
        logger.info("Rejected records: %s", rejected_count)

        logger.info(
            "Classified records:\n%s",
            df[[
                "order_id",
                "customer_name",
                "quantity",
                "price",
                "status"
            ]].to_string(index=False)
        )

        # 7. Verify classification totals
        assert valid_count + warning_count + rejected_count == len(df)

        logger.info("Classification verification successful")

        return df

    except Exception:
        logger.exception("Record classification failed")
        raise


def separate_records(df):

    try:

        valid_records = df[df["status"] == "VALID"]

        warning_records = df[df["status"] == "WARNING"]

        rejected_records = df[df["status"] == "REJECTED"]

        logger.info("========== RECORD SEPARATION ==========")

        logger.info("Valid records: %s", len(valid_records))
        logger.info("Warning records: %s", len(warning_records))
        logger.info("Rejected records: %s", len(rejected_records))

        logger.info(
            "Records ready for processing: %s",
            len(valid_records) + len(warning_records)
        )

        return valid_records, warning_records, rejected_records

    except Exception:
        logger.exception("Record separation failed")
        raise


def save_validation_results(valid, warnings, rejected):

    try:

        logger.info("Starting validation file saving")

        # Load configuration
        config = load_config()

        # Locate project directory
        project_dir = Path(__file__).resolve().parent.parent

        # Get output directories from configuration
        processed_dir = project_dir / config["directories"]["processed"]
        rejected_dir = project_dir / config["directories"]["rejected"]

        processed_dir.mkdir(parents=True, exist_ok=True)
        rejected_dir.mkdir(parents=True, exist_ok=True)

        # Get output filenames from configuration
        validation_files = config["validation_files"]

        # Save valid records
        valid_path = processed_dir / validation_files["valid"]
        valid.to_csv(valid_path, index=False)

        logger.info("Valid records saved: %s", valid_path)

        # Save warning records
        warning_path = processed_dir / validation_files["warnings"]
        warnings.to_csv(warning_path, index=False)

        logger.info("Warning records saved: %s", warning_path)

        # Save rejected records
        rejected_path = rejected_dir / validation_files["rejected"]
        rejected.to_csv(rejected_path, index=False)

        logger.info("Rejected records saved: %s", rejected_path)

        logger.info("Validation files saved successfully")

    except Exception:
        logger.exception("Saving validation files failed")
        raise


if __name__ == "__main__":

    # Extract raw data using configuration
    sales_data = extract_data()

    # Generate data quality report
    validate_data(sales_data)

    # Classify records
    classified_data = classify_records(sales_data)

    # Separate records
    valid_records, warning_records, rejected_records = separate_records(
        classified_data
    )

    # Save validation results
    save_validation_results(
        valid_records,
        warning_records,
        rejected_records
    )
