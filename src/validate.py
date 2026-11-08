
import pandas as pd

from extract import extract_data


def validate_data(df):

    print("\n========== DATA QUALITY REPORT ==========\n")

    total_records = len(df)

    print("Total records:", total_records)

    # 1. Check missing values
    print("\n1. MISSING VALUES")

    for column in df.columns:
        missing = df[column].isna().sum()
        print(f"{column}: {missing}")

    # 2. Check duplicate orders
    print("\n2. DUPLICATE ORDERS")

    duplicates = df["order_id"].duplicated().sum()

    print("Duplicate orders:", duplicates)

    # 3. Check invalid dates
    print("\n3. INVALID DATES")

    dates = pd.to_datetime(
        df["order_date"], errors="coerce"
    )

    print("Invalid dates:", dates.isna().sum())

    # 4. Check invalid numeric values
    print("\n4. INVALID NUMERIC VALUES")

    for column in ["quantity", "price"]:

        values = pd.to_numeric(
            df[column], errors="coerce"
        )

        invalid = (
            values.isna() & df[column].notna()
        ).sum()

        print(f"Invalid {column} values:", invalid)

    # 5. Check negative or zero values
    print("\n5. NON-POSITIVE VALUES")

    for column in ["quantity", "price"]:

        values = pd.to_numeric(
            df[column], errors="coerce"
        )

        non_positive = (
            (values <= 0) & values.notna()
        ).sum()

        print(f"Non-positive {column}:", non_positive)

    print("\n========== VALIDATION COMPLETED ==========\n")








def classify_records(df):

    print("\n========== RECORD CLASSIFICATION ==========\n")

    df = df.copy()

    # Convert columns to appropriate formats
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )

    df["price"] = pd.to_numeric(
        df["price"], errors="coerce"
    )

    # Identify duplicate orders
    duplicate_orders = df["order_id"].duplicated(
        keep="first"
    )

    # Identify critical errors
    critical_errors = (
        df["order_id"].isna()
        | df["order_date"].isna()
        | df["quantity"].isna()
        | df["price"].isna()
        | (df["quantity"] <= 0)
        | (df["price"] <= 0)
        | duplicate_orders
    )

    # Identify warnings
    warnings = (
        df["customer_name"].isna()
        | df["product"].isna()
        | df["category"].isna()
        | df["city"].isna()
    )

    df["status"] = "VALID"

    df.loc[warnings & ~critical_errors, "status"] = "WARNING"

    df.loc[critical_errors, "status"] = "REJECTED"

    print("Valid records:", (df["status"] == "VALID").sum())

    print("Warning records:", (df["status"] == "WARNING").sum())

    print("Rejected records:", (df["status"] == "REJECTED").sum())

    print("\nClassified records:")

    print(df[["order_id", "customer_name", "quantity", "price", "status"]])

    return df


def separate_records(df):

    valid_records = df[df["status"] == "VALID"]

    warning_records = df[df["status"] == "WARNING"]

    rejected_records = df[df["status"] == "REJECTED"]

    print("\n========== RECORD SEPARATION ==========\n")

    print("Valid records:", len(valid_records))
    print("Warning records:", len(warning_records))
    print("Rejected records:", len(rejected_records))

    print("\nRecords ready for processing:")
    print(len(valid_records) + len(warning_records))

    return valid_records, warning_records, rejected_records


from pathlib import Path


def save_validation_results(valid, warnings, rejected):

    project_dir = Path(__file__).resolve().parent.parent

    processed_dir = project_dir / "data" / "processed"
    rejected_dir = project_dir / "data" / "rejected"

    processed_dir.mkdir(parents=True, exist_ok=True)
    rejected_dir.mkdir(parents=True, exist_ok=True)

    valid.to_csv(
        processed_dir / "valid_records.csv",
        index=False
    )

    warnings.to_csv(
        processed_dir / "warning_records.csv",
        index=False
    )

    rejected.to_csv(
        rejected_dir / "rejected_records.csv",
        index=False
    )

    print("\n========== FILE SAVING REPORT ==========\n")

    print("Valid records saved successfully!")
    print("Warning records saved successfully!")
    print("Rejected records saved successfully!")


if __name__ == "__main__":

    from pathlib import Path

    project_dir = Path(__file__).resolve().parent.parent

    test_file = project_dir / "data" / "raw" / "retail_sales_test.csv"

    sales_data = pd.read_csv(test_file)

    validate_data(sales_data)

    classified_data = classify_records(sales_data)
    valid_records, warning_records, rejected_records = separate_records(classified_data)
    save_validation_results(
    valid_records,
    warning_records,
    rejected_records
)