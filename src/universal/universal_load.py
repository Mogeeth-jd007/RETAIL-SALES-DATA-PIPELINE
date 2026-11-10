
import re
import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def sanitize_table_name(name):
    """Convert a dataset name into a safe SQLite table name."""

    table_name = re.sub(r"[^a-zA-Z0-9_]", "_", str(name).lower())
    table_name = re.sub(r"_+", "_", table_name).strip("_")

    if not table_name:
        table_name = "dataset"

    if table_name[0].isdigit():
        table_name = f"dataset_{table_name}"

    return table_name


def load_universal(
    df,
    table_name,
    database_path=None,
    if_exists="replace"
):
    """
    Load a DataFrame into a dynamically created SQLite table.

    No dataset profile or predefined table schema is required.
    """

    if if_exists not in {"replace", "append", "fail"}:
        raise ValueError("if_exists must be replace, append, or fail")

    table_name = sanitize_table_name(table_name)

    if database_path is None:
        database_path = PROJECT_ROOT / "data" / "universal_pipeline.db"
    else:
        database_path = Path(database_path)

        if not database_path.is_absolute():
            database_path = PROJECT_ROOT / database_path

    database_path.parent.mkdir(parents=True, exist_ok=True)

    print("\n========== UNIVERSAL DATABASE LOAD STARTED ==========")

    with sqlite3.connect(database_path) as connection:

        df.to_sql(
            name=table_name,
            con=connection,
            if_exists=if_exists,
            index=False
        )

        loaded_count = len(df)

        table_info = pd.read_sql_query(
            f'PRAGMA table_info("{table_name}")',
            connection
        )

    print(f"Database: {database_path}")
    print(f"Table: {table_name}")
    print(f"Records loaded: {loaded_count}")

    print("\nDYNAMIC TABLE STRUCTURE:")
    print(table_info[["name", "type"]])

    print("\n========== UNIVERSAL DATABASE LOAD COMPLETED ==========\n")

    return {
        "database_path": str(database_path),
        "table_name": table_name,
        "records_loaded": loaded_count,
        "columns": table_info["name"].tolist()
    }
