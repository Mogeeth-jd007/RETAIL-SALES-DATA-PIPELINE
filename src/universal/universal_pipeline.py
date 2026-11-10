
from pathlib import Path

import pandas as pd

from .universal_transform import transform_universal
from .universal_validate import validate_universal
from .universal_load import load_universal
from .report_generator import generate_reports


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def resolve_input_file(input_file):
    """Resolve absolute, project-relative and raw-folder CSV paths."""

    path = Path(input_file)

    if path.is_absolute():
        resolved_path = path
    else:
        candidates = [
            PROJECT_ROOT / path,
            PROJECT_ROOT / "data" / "raw" / path
        ]

        resolved_path = next(
            (candidate for candidate in candidates if candidate.is_file()),
            None
        )

    if resolved_path is None or not resolved_path.is_file():
        raise FileNotFoundError(
            f"Input CSV not found: {input_file}"
        )

    if resolved_path.suffix.lower() != ".csv":
        raise ValueError("Universal pipeline currently accepts CSV files only.")

    return resolved_path


def run_universal_pipeline(input_file):
    """
    Execute the complete universal ETL pipeline.

    No dataset profiles or manual column configurations are required.
    """

    print("\n")
    print("=" * 60)
    print("       UNIVERSAL AUTOMATED ETL PIPELINE")
    print("=" * 60)

    # Resolve the input file.
    file_path = resolve_input_file(input_file)
    dataset_name = file_path.stem

    print(f"\nInput file: {file_path}")
    print(f"Dataset name: {dataset_name}")

    # STEP 1: EXTRACTION
    print("\n[STEP 1/5] EXTRACTING DATA")

    df = pd.read_csv(file_path)

    print(f"Records extracted: {len(df)}")
    print(f"Columns extracted: {len(df.columns)}")

    # STEP 2: TRANSFORMATION
    print("\n[STEP 2/5] TRANSFORMING DATA")

    transformed_df, schema = transform_universal(df)

    # STEP 3: VALIDATION
    print("\n[STEP 3/5] VALIDATING DATA")

    valid, warning, rejected, report = validate_universal(
        transformed_df
    )

    # STEP 4: DATABASE LOADING
    print("\n[STEP 4/5] LOADING DATABASE")

    eligible_records = pd.concat(
        [valid, warning]
    ).sort_index()

    database_result = load_universal(
        eligible_records,
        table_name=dataset_name
    )

    # STEP 5: REPORT GENERATION
    print("\n[STEP 5/5] GENERATING REPORTS")

    report_files = generate_reports(
        valid,
        warning,
        rejected,
        report,
        schema,
        dataset_name
    )

    # FINAL SUMMARY
    print("\n")
    print("=" * 60)
    print("       UNIVERSAL ETL PIPELINE COMPLETED")
    print("=" * 60)

    print(f"Dataset: {dataset_name}")
    print(f"Total records: {report['total_records']}")
    print(f"Valid records: {report['valid_records']}")
    print(f"Warning records: {report['warning_records']}")
    print(f"Rejected records: {report['rejected_records']}")
    print(f"Database table: {database_result['table_name']}")

    print("\nAll pipeline stages completed successfully.")

    return {
        "dataset": dataset_name,
        "quality_report": report,
        "database": database_result,
        "files": report_files
    }
