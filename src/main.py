
import pandas as pd

from extract import extract_data
from transform import transform_data
from validate import (
    validate_data,
    classify_records,
    separate_records,
    save_validation_results
)
from load import load_data
from config import load_config
from logger import get_logger


# Initialize logger
logger = get_logger("MAIN")


def run_pipeline():

    logger.info("========== RETAIL SALES ETL PIPELINE STARTED ==========")

    try:

        # Load project configuration
        logger.info("Loading project configuration")

        config = load_config()

        # STEP 1: EXTRACT
        logger.info("STEP 1: EXTRACT")

        input_file = config["input_file"]
        df = extract_data(input_file)

        logger.info("Extraction completed successfully")

        # STEP 2: TRANSFORM
        logger.info("STEP 2: TRANSFORM")

        transformed_df = transform_data(df)

        logger.info("Transformation completed successfully")

        # STEP 3: VALIDATE
        logger.info("STEP 3: VALIDATE")

        validate_data(transformed_df)

        logger.info("Validation completed successfully")

        # STEP 4: CLASSIFY
        logger.info("STEP 4: CLASSIFY")

        classified_df = classify_records(transformed_df)

        logger.info("Classification completed successfully")

        # STEP 5: SEPARATE RECORDS
        logger.info("STEP 5: SEPARATE RECORDS")

        valid_records, warning_records, rejected_records = (
            separate_records(classified_df)
        )

        logger.info(
            "Record separation completed: Valid=%s, Warnings=%s, Rejected=%s",
            len(valid_records),
            len(warning_records),
            len(rejected_records)
        )

        # STEP 6: SAVE VALIDATION RESULTS
        logger.info("STEP 6: SAVE VALIDATION FILES")

        save_validation_results(
            valid_records,
            warning_records,
            rejected_records
        )

        logger.info("Validation files saved successfully")

        # STEP 7: LOAD ELIGIBLE RECORDS
        logger.info("STEP 7: LOAD")

        records_to_load = pd.concat(
            [valid_records, warning_records],
            ignore_index=True
        )

        # Remove classification column
        records_to_load = records_to_load.drop(
            columns=["status"],
            errors="ignore"
        )

        # Convert dates into SQLite-friendly strings
        if "order_date" in records_to_load.columns:
            records_to_load["order_date"] = (
                records_to_load["order_date"].astype(str)
            )

        load_data(records_to_load)

        logger.info("Loading completed successfully")

        logger.info("========== ETL PIPELINE COMPLETED SUCCESSFULLY ==========")

    except Exception:
        logger.exception("ETL PIPELINE FAILED")
        raise


if __name__ == "__main__":
    run_pipeline()
