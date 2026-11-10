
import argparse
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
from config import load_config, load_dataset_config
from logger import get_logger


logger = get_logger("MAIN")


def run_pipeline(dataset_name=None, input_file=None):

    try:

        # Load project configuration
        config = load_config()

        if dataset_name is None:
            dataset_name = config["active_dataset"]

        # Validate selected dataset profile
        dataset_config = load_dataset_config(dataset_name)

        logger.info("========== ETL PIPELINE STARTED ==========")
        logger.info("Selected dataset: %s", dataset_name)

        # STEP 1: EXTRACT
        logger.info("STEP 1: EXTRACT")

        df = extract_data(
            filename=input_file,
            dataset_name=dataset_name
        )

        logger.info("Extraction completed successfully")

        # STEP 2: TRANSFORM
        logger.info("STEP 2: TRANSFORM")

        transformed_df = transform_data(
            df,
            dataset_name=dataset_name
        )

        logger.info("Transformation completed successfully")

        # STEP 3: VALIDATE
        logger.info("STEP 3: VALIDATE")

        validate_data(
            transformed_df,
            dataset_name=dataset_name
        )

        logger.info("Validation completed successfully")

        # STEP 4: CLASSIFY
        logger.info("STEP 4: CLASSIFY")

        classified_df = classify_records(
            transformed_df,
            dataset_name=dataset_name
        )

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
            rejected_records,
            dataset_name=dataset_name
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

        # Convert configured dates into SQLite-friendly strings
        date_columns = dataset_config["transformation"].get(
            "date_columns",
            []
        )

        for column in date_columns:

            if column in records_to_load.columns:
                records_to_load[column] = (
                    records_to_load[column].astype(str)
                )

        load_data(
            records_to_load,
            dataset_name=dataset_name
        )

        logger.info("Loading completed successfully")

        logger.info(
            "========== ETL PIPELINE COMPLETED SUCCESSFULLY =========="
        )

    except Exception:
        logger.exception("ETL PIPELINE FAILED")
        raise


if __name__ == "__main__":

    # Command-line arguments
    parser = argparse.ArgumentParser(
        description="Multi-dataset ETL Pipeline"
    )

    parser.add_argument(
        "--dataset",
        choices=["retail", "employee", "student"],
        default=None,
        help="Dataset profile to process"
    )

    parser.add_argument(
        "--file",
        default=None,
        help="Optional CSV filename override"
    )

    args = parser.parse_args()

    run_pipeline(
        dataset_name=args.dataset,
        input_file=args.file
    )
