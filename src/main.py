
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


def run_pipeline():

    print("\n========== RETAIL SALES ETL PIPELINE ==========\n")

    # STEP 1: EXTRACT
    print("STEP 1: EXTRACT")
    df = extract_data("retail_sales_test.csv")

    # STEP 2: TRANSFORM
    print("\nSTEP 2: TRANSFORM")
    transformed_df = transform_data(df)

    # STEP 3: VALIDATE
    print("\nSTEP 3: VALIDATE")
    validate_data(transformed_df)

    # STEP 4: CLASSIFY
    print("\nSTEP 4: CLASSIFY")
    classified_df = classify_records(transformed_df)

    # STEP 5: SEPARATE RECORDS
    print("\nSTEP 5: SEPARATE RECORDS")
    valid_records, warning_records, rejected_records = (
        separate_records(classified_df)
    )

    # STEP 6: SAVE VALIDATION RESULTS
    print("\nSTEP 6: SAVE VALIDATION FILES")

    save_validation_results(
        valid_records,
        warning_records,
        rejected_records
    )

    # STEP 7: LOAD ELIGIBLE RECORDS
    print("\nSTEP 7: LOAD")

    records_to_load = pd.concat(
        [valid_records, warning_records],
        ignore_index=True
    )

    # Remove classification column before database loading
    records_to_load = records_to_load.drop(
        columns=["status"],
        errors="ignore"
    )

    # Convert dates into SQLite-friendly strings
    records_to_load["order_date"] = (
        records_to_load["order_date"].astype(str)
    )

    load_data(records_to_load)

    print("\n========== ETL PIPELINE COMPLETED ==========\n")


if __name__ == "__main__":
    run_pipeline()
