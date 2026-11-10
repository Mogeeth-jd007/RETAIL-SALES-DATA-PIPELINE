import pandas as pd
import pytest
from extract import extract_data


def test_extract_existing_csv():
    df = extract_data("retail_sales.csv")

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "order_id" in df.columns

def test_extract_missing_csv():
    with pytest.raises(FileNotFoundError):
        extract_data("missing_file.csv")