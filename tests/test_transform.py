import pandas as pd
from transform import standardize_column_names


def test_standardize_column_names():
    df = pd.DataFrame(columns=[
        "Customer Name",
        "Order-Date",
        "Product Name",
        "Total Price"
    ])

    result = standardize_column_names(df)

    assert list(result.columns) == [
        "customer_name",
        "order_date",
        "product_name",
        "total_price"
    ]

from transform import clean_text_columns


def test_clean_text_columns():
    df = pd.DataFrame({
        "customer_name": [" Rahul ", " Arun ", "   "],
        "city": [" Chennai ", " Bangalore ", " Coimbatore "]
    })

    result = clean_text_columns(df)

    assert result["customer_name"].iloc[0] == "Rahul"
    assert result["customer_name"].iloc[1] == "Arun"
    assert pd.isna(result["customer_name"].iloc[2])
    assert result["city"].iloc[0] == "Chennai"

from transform import detect_data_types


def test_detect_data_types():
    df = pd.DataFrame({
        "quantity": ["100", "200", "300", "UNKNOWN", "UNKNOWN"],
        "price": ["100", "200", "300", "400", "UNKNOWN"],
        "customer_id": ["101", "102", "103", "104", "105"]
    })

    result = detect_data_types(df)

    assert pd.api.types.is_numeric_dtype(result["quantity"]) is False
    assert pd.api.types.is_numeric_dtype(result["price"])
    assert not pd.api.types.is_numeric_dtype(result["customer_id"])

from transform import transform_data


def test_transform_data():
    df = pd.DataFrame({
        "order_id": ["1001", "1002"],
        "order_date": ["2026-01-01", "2026-01-02"],
        "quantity": ["2", "3"],
        "price": ["100", "200"]
    })

    result = transform_data(df)

    assert len(result) == 2
    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])
    assert result["total_amount"].tolist() == [200, 600]
