import pandas as pd
from validate import classify_records
def test_warning_record():
    df = pd.DataFrame({
        "order_id": [1002],
        "order_date": ["2026-01-02"],
        "customer_name": [None],
        "product": ["Mouse"],
        "category": ["Accessories"],
        "quantity": [3],
        "price": [500],
        "city": ["Bangalore"]
    })

    result = classify_records(df)

    assert result["status"].iloc[0] == "WARNING"

def test_valid_record():
    df = pd.DataFrame({
        "order_id": [1001],
        "order_date": ["2026-01-01"],
        "customer_name": ["Rahul"],
        "product": ["Laptop"],
        "category": ["Electronics"],
        "quantity": [2],
        "price": [45000],
        "city": ["Chennai"]
    })

    result = classify_records(df)

    assert result["status"].iloc[0] == "VALID"

def test_rejected_record():
    df = pd.DataFrame({
        "order_id": [1003],
        "order_date": ["2026-01-03"],
        "customer_name": ["Priya"],
        "product": ["Keyboard"],
        "category": ["Accessories"],
        "quantity": [-1],
        "price": [1200],
        "city": ["Coimbatore"]
    })

    result = classify_records(df)

    assert result["status"].iloc[0] == "REJECTED"

def test_duplicate_order_id():
    df = pd.DataFrame({
        "order_id": [1004, 1004],
        "order_date": ["2026-01-04", "2026-01-05"],
        "customer_name": ["Kumar", "Arun"],
        "product": ["Monitor", "Mouse"],
        "category": ["Electronics", "Accessories"],
        "quantity": [1, 2],
        "price": [12000, 500],
        "city": ["Chennai", "Bangalore"]
    })

    result = classify_records(df)

    assert result["status"].tolist() == ["VALID", "REJECTED"]

def test_missing_required_value():
    df = pd.DataFrame({
        "order_id": [None],
        "order_date": ["2026-01-06"],
        "customer_name": ["Meena"],
        "product": ["Mobile"],
        "category": ["Electronics"],
        "quantity": [2],
        "price": [15000],
        "city": ["Madurai"]
    })

    result = classify_records(df)

    assert result["status"].iloc[0] == "REJECTED"