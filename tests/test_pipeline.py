import sqlite3
import sys
import pandas as pd

import main
import validate
import load


def test_clean_dataset_pipeline(tmp_path, monkeypatch):

    processed_dir = tmp_path / "processed"
    rejected_dir = tmp_path / "rejected"
    database_file = tmp_path / "test.db"

    processed_dir.mkdir()
    rejected_dir.mkdir()

    config = validate.load_config()
    test_config = config.copy()

    test_config["directories"] = {
        "processed": str(processed_dir),
        "rejected": str(rejected_dir)
    }

    test_config["database"] = {
        "file": str(database_file),
        "table": "test_sales"
    }

    monkeypatch.setattr(
        main, "load_config", lambda: test_config
    )

    monkeypatch.setattr(
        validate, "load_config", lambda: test_config
    )

    monkeypatch.setattr(
        load, "load_config", lambda: test_config
    )

    # Redirect validation output files to temporary folders
    def save_test_outputs(valid, warnings, rejected):

        files = test_config["validation_files"]

        valid.to_csv(
            processed_dir / files["valid"], index=False
        )

        warnings.to_csv(
            processed_dir / files["warnings"], index=False
        )

        rejected.to_csv(
            rejected_dir / files["rejected"], index=False
        )

    monkeypatch.setattr(
        main, "save_validation_results", save_test_outputs
    )

    # Select the clean dataset
    monkeypatch.setattr(
        sys, "argv", ["main.py", "retail_sales.csv"]
    )

    # Run the complete pipeline
    main.run_pipeline()

    # Verify output files
    files = test_config["validation_files"]

    assert (processed_dir / files["valid"]).exists()
    assert (processed_dir / files["warnings"]).exists()
    assert (rejected_dir / files["rejected"]).exists()

    # Verify SQLite records
    conn = sqlite3.connect(database_file)

    try:
        result = pd.read_sql_query(
            "SELECT * FROM test_sales", conn
        )
    finally:
        conn.close()

    assert len(result) == 10

def test_dirty_dataset_pipeline(tmp_path, monkeypatch):

    processed_dir = tmp_path / "processed"
    rejected_dir = tmp_path / "rejected"
    database_file = tmp_path / "test.db"

    processed_dir.mkdir()
    rejected_dir.mkdir()

    config = validate.load_config()
    test_config = config.copy()

    test_config["directories"] = {
        "processed": str(processed_dir),
        "rejected": str(rejected_dir)
    }

    test_config["database"] = {
        "file": str(database_file),
        "table": "test_sales"
    }

    monkeypatch.setattr(
        main, "load_config", lambda: test_config
    )

    monkeypatch.setattr(
        validate, "load_config", lambda: test_config
    )

    monkeypatch.setattr(
        load, "load_config", lambda: test_config
    )

    def save_test_outputs(valid, warnings, rejected):

        files = test_config["validation_files"]

        valid.to_csv(
            processed_dir / files["valid"], index=False
        )

        warnings.to_csv(
            processed_dir / files["warnings"], index=False
        )

        rejected.to_csv(
            rejected_dir / files["rejected"], index=False
        )

    monkeypatch.setattr(
        main, "save_validation_results", save_test_outputs
    )

    # Select the dirty dataset
    monkeypatch.setattr(
        sys, "argv", ["main.py", "retail_sales_test.csv"]
    )

    # Run the complete pipeline
    main.run_pipeline()

    files = test_config["validation_files"]

    valid_df = pd.read_csv(
        processed_dir / files["valid"]
    )

    warning_df = pd.read_csv(
        processed_dir / files["warnings"]
    )

    rejected_df = pd.read_csv(
        rejected_dir / files["rejected"]
    )

    # Verify record classifications
    assert len(valid_df) == 1
    assert len(warning_df) == 1
    assert len(rejected_df) == 7

    # Verify SQLite records
    conn = sqlite3.connect(database_file)

    try:
        result = pd.read_sql_query(
            "SELECT * FROM test_sales", conn
        )
    finally:
        conn.close()

    assert len(result) == 2