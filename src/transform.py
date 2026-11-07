
import pandas as pd
from pathlib import Path

from extract import extract_data


def transform_data(df):

    # Remove unnecessary spaces from column names
    df.columns = df.columns.str.strip().str.lower()

    # Remove duplicate orders
    df = df.drop_duplicates(subset=["order_id"])

    # Clean text columns
    for column in ["customer_name", "product", "category", "city"]:
        df[column] = df[column].astype("string").str.strip()

    # Convert columns into correct data types
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )

    df["price"] = pd.to_numeric(
        df["price"], errors="coerce"
    )

    # Remove records with missing essential values
    df = df.dropna(
        subset=["order_id", "order_date", "product", "quantity", "price"]
    )

    # Calculate total sales
    df["total_amount"] = df["quantity"] * df["price"]

    print("Data transformation completed!")

    return df


if __name__ == "__main__":

    # Extract raw data
    sales_data = extract_data()

    # Transform raw data
    cleaned_data = transform_data(sales_data)

    # Create processed folder
    project_dir = Path(__file__).resolve().parent.parent
    output_dir = project_dir / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save transformed data
    output_file = output_dir / "cleaned_retail_sales.csv"
    cleaned_data.to_csv(output_file, index=False)

    print("\nTransformed data:")
    print(cleaned_data)

    print("\nTotal records:", len(cleaned_data))
    print("\nTotal sales:", cleaned_data["total_amount"].sum())

    print("\nProcessed file saved at:", output_file)
