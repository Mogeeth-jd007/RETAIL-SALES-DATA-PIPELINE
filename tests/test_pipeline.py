
import sqlite3
import pandas as pd

import main
import validate
import load


def setup_test_environment(tmp_path, monkeypatch):

    processed_dir = tmp_path / "processed"
    rejected_dir = tmp_path / "rejected"
    database_file = tmp_path / "test.db"

    processed_dir.mkdir()
    rejected_dir.mkdir()

    # Redirect database to a temporary location
    monkeypatch.setattr(
        load,
        "get_project_path",
        lambda path: database_file
    )

    # Redirect validation output files
    def save_test_outputs(
    valid,
    warnings,
    rejected,
    dataset_name=None
    ):

        files = validate.load_dataset_config(
            dataset_name
        )["validation_files"]

        valid.to_csv(
            processed_dir / files["valid"],
            index=False
        )

        warnings.to_csv(
            processed_dir / files["warnings"],
            index=False
        )

        rejected.to_csv(
            rejected_dir / files["rejected"],
            index=False
        )

    monkeypatch.setattr(
        main,
        "save_validation_results",
        save_test_outputs
    )

    return processed_dir, rejected_dir, database_file


def test_clean_dataset_pipeline(tmp_path, monkeypatch):

    processed_dir, rejected_dir, database_file = (
        setup_test_environment(tmp_path, monkeypatch)
    )

    # Run clean retail pipeline
    main.run_pipeline(
        dataset_name="retail",
        input_file="retail_sales.csv"
    )

    files = validate.load_dataset_config(
        "retail"
    )["validation_files"]

    # Verify output files
    assert (processed_dir / files["valid"]).exists()
    assert (processed_dir / files["warnings"]).exists()
    assert (rejected_dir / files["rejected"]).exists()

    # Verify SQLite records
    with sqlite3.connect(database_file) as conn:

        result = pd.read_sql_query(
            "SELECT * FROM retail_sales",
            conn
        )

    assert len(result) == 10


def test_dirty_dataset_pipeline(tmp_path, monkeypatch):

    processed_dir, rejected_dir, database_file = (
        setup_test_environment(tmp_path, monkeypatch)
    )

    # Run dirty retail pipeline
    main.run_pipeline(
        dataset_name="retail",
        input_file="retail_sales_test.csv"
    )

    files = validate.load_dataset_config(
        "retail"
    )["validation_files"]

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
    with sqlite3.connect(database_file) as conn:

        result = pd.read_sql_query(
            "SELECT * FROM retail_sales",
            conn
        )

    assert len(result) == 2
def test_employee_dataset_pipeline(tmp_path, monkeypatch):

    processed_dir, rejected_dir, database_file = (
        setup_test_environment(tmp_path, monkeypatch)
    )

    # Run employee pipeline
    main.run_pipeline(dataset_name="employee")

    # Verify employee database
    with sqlite3.connect(database_file) as conn:
        result = pd.read_sql_query(
            "SELECT * FROM employees",
            conn
        )

    assert len(result) == 9


def test_student_dataset_pipeline(tmp_path, monkeypatch):

    processed_dir, rejected_dir, database_file = (
        setup_test_environment(tmp_path, monkeypatch)
    )

    # Run student pipeline
    main.run_pipeline(dataset_name="student")

    # Verify student database
    with sqlite3.connect(database_file) as conn:
        result = pd.read_sql_query(
            "SELECT * FROM students",
            conn
        )

    assert len(result) == 9