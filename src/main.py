
from extract import extract_data
from transform import transform_data
from load import load_data


def run_pipeline():

    print("\n========== RETAIL SALES ETL PIPELINE ==========\n")

    # STEP 1: EXTRACT
    print("STEP 1: EXTRACT")
    df = extract_data()

    # STEP 2: TRANSFORM
    print("\nSTEP 2: TRANSFORM")
    transformed_df = transform_data(df)

    # STEP 3: LOAD
    print("\nSTEP 3: LOAD")
    load_data(transformed_df)

    print("\n========== ETL PIPELINE COMPLETED ==========\n")


if __name__ == "__main__":
    run_pipeline()
