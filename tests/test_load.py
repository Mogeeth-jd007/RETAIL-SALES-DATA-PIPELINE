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

    monkeypatch.setattr("load.load_config", lambda: test_config)
    monkeypatch.setattr(
        "load.get_project_path",
        lambda path: database_file
    )

    df = pd.DataFrame({
        "order_id": [1001, 1002],
        "quantity": [2, 3],
        "price": [100, 200]
    })

    load_data(df)

    conn = sqlite3.connect(database_file)

    result = pd.read_sql_query(
        "SELECT * FROM test_sales",
        conn
    )

    conn.close()

    assert len(result) == 2
    assert result["order_id"].tolist() == [1001, 1002]