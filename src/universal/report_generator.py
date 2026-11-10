
import json
import re
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def safe_filename(name):
    """Generate a safe filename from the input dataset name."""

    name = re.sub(r"[^a-zA-Z0-9_-]", "_", str(name))
    name = re.sub(r"_+", "_", name).strip("_")

    return name or "dataset"


def generate_reports(
    valid_records,
    warning_records,
    rejected_records,
    report,
    schema,
    dataset_name
):
    """
    Generate processed CSVs, rejected CSVs and a JSON quality report.
    """

    print("\n========== REPORT GENERATION STARTED ==========")

    dataset_name = safe_filename(dataset_name)

    processed_dir = PROJECT_ROOT / "data" / "processed"
    rejected_dir = PROJECT_ROOT / "data" / "rejected"
    reports_dir = PROJECT_ROOT / "reports"

    processed_dir.mkdir(parents=True, exist_ok=True)
    rejected_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    processed_records = pd.concat(
        [valid_records, warning_records]
    ).sort_index()

    # Save processed records.
    processed_path = processed_dir / f"{dataset_name}_processed.csv"
    processed_records.to_csv(processed_path, index=False)

    # Save valid records.
    valid_path = processed_dir / f"{dataset_name}_valid.csv"
    valid_records.to_csv(valid_path, index=False)

    # Save warning records.
    warning_path = processed_dir / f"{dataset_name}_warnings.csv"
    warning_records.to_csv(warning_path, index=False)

    # Save rejected records.
    rejected_path = rejected_dir / f"{dataset_name}_rejected.csv"
    rejected_records.to_csv(rejected_path, index=False)

    # Combine quality statistics and detected schema.
    quality_report = {
        "dataset": dataset_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "quality_summary": report,
        "detected_schema": schema
    }

    report_path = reports_dir / f"{dataset_name}_quality_report.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(quality_report, file, indent=4, default=str)

    print("Processed CSV saved:", processed_path)
    print("Valid CSV saved:", valid_path)
    print("Warning CSV saved:", warning_path)
    print("Rejected CSV saved:", rejected_path)
    print("Quality report saved:", report_path)

    print("\n========== REPORT GENERATION COMPLETED ==========\n")

    return {
        "processed_file": str(processed_path),
        "valid_file": str(valid_path),
        "warning_file": str(warning_path),
        "rejected_file": str(rejected_path),
        "quality_report": str(report_path)
    }
