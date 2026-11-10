import sqlite3
import pandas as pd

from load import load_data


def test_load_data_to_sqlite(tmp_path, monkeypatch):

    database_file = tmp_path / "test_retail_sales.db"

    test_config = {
        "database": {
            "file": "test_retail_sales.db",
            "table": "test_sales"
        }
    }

    # Mock dataset configuration
    monkeypatch.setattr(
        "load.load_dataset_config",
        lambda dataset_name=None: test_config
    )

    # Mock database path
    monkeypatch.setattr(
        "load.get_project_path",
        lambda path: database_file
    )

    df = pd.DataFrame({
        "order_id": [1001, 1002],
        "quantity": [2, 3],
        "price": [100, 200]
    })

    # Execute database loading
    load_data(df, dataset_name="retail")

    # Verify database contents
    with sqlite3.connect(database_file) as conn:

        result = pd.read_sql_query(
            "SELECT * FROM test_sales",
            conn
        )

    assert len(result) == 2
    assert result["order_id"].tolist() == [1001, 1002]