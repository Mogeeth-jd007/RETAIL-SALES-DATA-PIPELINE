
import pandas as pd
from pathlib import Path

from extract import extract_data
from config import load_config, load_dataset_config
from logger import get_logger


logger = get_logger("VALIDATE")


def get_validation_rules(dataset_name=None):

    dataset_config = load_dataset_config(dataset_name)

    return dataset_config["validation"]


def validate_data(df, dataset_name=None):

    try:

        logger.info("========== DATA QUALITY REPORT ==========")

        rules = get_validation_rules(dataset_name)

        total_records = len(df)

        logger.info("Total records: %s", total_records)

        configured_columns = (
            rules["required_columns"]
            + rules["warning_columns"]
            + rules["positive_columns"]
            + rules["date_columns"]
            + rules["unique_columns"]
        )

        missing_columns = [
            column for column in set(configured_columns)
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Configured columns missing from dataset: {missing_columns}"
            )

        # 1. Missing values
        logger.info("1. MISSING VALUES")

        for column in df.columns:

            missing = df[column].isna().sum()

            logger.info(
                "%s: %s missing values",
                column,
                missing
            )

        # 2. Duplicate checks
        logger.info("2. DUPLICATE CHECKS")

        for column in rules["unique_columns"]:

            duplicates = (
                df[column].notna()
                & df[column].duplicated()
            ).sum()

            logger.info(
                "Duplicate %s values: %s",
                column,
                duplicates
            )

        # 3. Date validation
        logger.info("3. DATE VALIDATION")

        for column in rules["date_columns"]:

            dates = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            invalid_dates = dates.isna().sum()

            logger.info(
                "Missing or invalid %s values: %s",
                column,
                invalid_dates
            )

        # 4. Numeric validation
        logger.info("4. NUMERIC VALIDATION")

        for column in rules["positive_columns"]:

            values = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            invalid = values.isna().sum()

            logger.info(
                "Missing or invalid %s values: %s",
                column,
                invalid
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


def classify_records(df, dataset_name=None):

    try:

        logger.info("Starting record classification")

        df = df.copy()

        rules = get_validation_rules(dataset_name)

        configured_columns = (
            rules["required_columns"]
            + rules["warning_columns"]
            + rules["positive_columns"]
            + rules["date_columns"]
            + rules["unique_columns"]
        )

        missing_columns = [
            column for column in set(configured_columns)
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Configured columns missing from dataset: {missing_columns}"
            )

        # 1. Convert configured date columns
        for column in rules["date_columns"]:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

        # 2. Convert configured numeric columns
        for column in rules["positive_columns"]:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        # 3. Initialize error masks
        critical_errors = pd.Series(False, index=df.index)
        warnings = pd.Series(False, index=df.index)

        # 4. Check required values
        for column in rules["required_columns"]:

            critical_errors |= df[column].isna()

        # 5. Check dates
        for column in rules["date_columns"]:

            critical_errors |= df[column].isna()

        # 6. Check positive numeric values
        for column in rules["positive_columns"]:

            critical_errors |= (
                df[column].isna() | (df[column] <= 0)
            )

        # 7. Check duplicate identifiers
        for column in rules["unique_columns"]:

            duplicates = (
                df[column].notna()
                & df[column].duplicated(keep="first")
            )

            critical_errors |= duplicates

        # 8. Check warning columns
        for column in rules["warning_columns"]:

            warnings |= df[column].isna()

        # 9. Assign classification
        df["status"] = "VALID"

        df.loc[
            warnings & ~critical_errors,
            "status"
        ] = "WARNING"

        df.loc[
            critical_errors,
            "status"
        ] = "REJECTED"

        # 10. Classification summary
        valid_count = (df["status"] == "VALID").sum()
        warning_count = (df["status"] == "WARNING").sum()
        rejected_count = (df["status"] == "REJECTED").sum()

        logger.info("Valid records: %s", valid_count)
        logger.info("Warning records: %s", warning_count)
        logger.info("Rejected records: %s", rejected_count)

        # 11. Dynamic preview
        preview_columns = list(dict.fromkeys(
            rules["required_columns"]
            + rules["warning_columns"]
            + rules["positive_columns"]
            + ["status"]
        ))

        logger.info(
            "Classified records:\n%s",
            df[preview_columns].to_string(index=False)
        )

        # 12. Verify classification totals
        assert (
            valid_count + warning_count + rejected_count
            == len(df)
        )

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


def save_validation_results(
    valid,
    warnings,
    rejected,
    dataset_name=None
):

    try:

        logger.info("Starting validation file saving")

        config = load_config()

        dataset_config = load_dataset_config(dataset_name)

        project_dir = Path(__file__).resolve().parent.parent

        processed_dir = (
            project_dir / config["directories"]["processed"]
        )

        rejected_dir = (
            project_dir / config["directories"]["rejected"]
        )

        processed_dir.mkdir(parents=True, exist_ok=True)
        rejected_dir.mkdir(parents=True, exist_ok=True)

        validation_files = dataset_config["validation_files"]

        # Save valid records
        valid_path = processed_dir / validation_files["valid"]

        valid.to_csv(valid_path, index=False)

        logger.info("Valid records saved: %s", valid_path)

        # Save warning records
        warning_path = (
            processed_dir / validation_files["warnings"]
        )

        warnings.to_csv(warning_path, index=False)

        logger.info("Warning records saved: %s", warning_path)

        # Save rejected records
        rejected_path = (
            rejected_dir / validation_files["rejected"]
        )

        rejected.to_csv(rejected_path, index=False)

        logger.info("Rejected records saved: %s", rejected_path)

        logger.info("Validation files saved successfully")

    except Exception:
        logger.exception("Saving validation files failed")
        raise


if __name__ == "__main__":

    config = load_config()

    dataset_name = config["active_dataset"]

    sales_data = extract_data(
        dataset_name=dataset_name
    )

    validate_data(
        sales_data,
        dataset_name=dataset_name
    )

    classified_data = classify_records(
        sales_data,
        dataset_name=dataset_name
    )

    valid_records, warning_records, rejected_records = (
        separate_records(classified_data)
    )

    save_validation_results(
        valid_records,
        warning_records,
        rejected_records,
        dataset_name=dataset_name
    )
