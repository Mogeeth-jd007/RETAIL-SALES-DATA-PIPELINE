
import pandas as pd


def validate_universal(df):
    """
    Validate an unknown dataset without requiring dataset profiles.

    Rules:
    1. Completely empty rows are REJECTED.
    2. Duplicate rows are REJECTED.
    3. Rows containing missing values are WARNING.
    4. Other rows are VALID.
    """

    print("\n========== UNIVERSAL VALIDATION STARTED ==========")

    df = df.copy()

    # Identify completely empty rows.
    empty_rows = df.isna().all(axis=1)

    # Identify duplicate rows, keeping the first occurrence.
    duplicate_rows = df.duplicated(keep="first")

    # Identify rows containing at least one missing value.
    missing_rows = df.isna().any(axis=1)

    # Assign initial status.
    df["quality_status"] = "VALID"

    # Missing values generate warnings.
    df.loc[missing_rows, "quality_status"] = "WARNING"

    # Duplicate rows are rejected.
    df.loc[duplicate_rows, "quality_status"] = "REJECTED"

    # Completely empty rows are rejected.
    df.loc[empty_rows, "quality_status"] = "REJECTED"

    # Separate records.
    valid_records = df[df["quality_status"] == "VALID"].copy()
    warning_records = df[df["quality_status"] == "WARNING"].copy()
    rejected_records = df[df["quality_status"] == "REJECTED"].copy()

    report = {
        "total_records": int(len(df)),
        "valid_records": int(len(valid_records)),
        "warning_records": int(len(warning_records)),
        "rejected_records": int(len(rejected_records)),
        "missing_value_rows": int(missing_rows.sum()),
        "duplicate_rows": int(duplicate_rows.sum()),
        "empty_rows": int(empty_rows.sum())
    }

    print("\nDATA QUALITY REPORT")

    for key, value in report.items():
        print(f"{key}: {value}")

    print("\n========== UNIVERSAL VALIDATION COMPLETED ==========\n")

    return (
        valid_records,
        warning_records,
        rejected_records,
        report
    )
