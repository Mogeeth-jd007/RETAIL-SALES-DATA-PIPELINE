
import pandas as pd
import re


def standardize_column_names(df):
    """Convert column names into consistent snake_case format."""

    df = df.copy()
    standardized = []

    for column in df.columns:
        name = str(column).strip().lower()
        name = re.sub(r"[^a-z0-9]+", "_", name)
        name = re.sub(r"_+", "_", name)
        name = name.strip("_")
        standardized.append(name)

    df.columns = standardized

    return df


def looks_like_date(values):
    """Check whether values resemble common date formats."""

    samples = values.dropna().astype(str).str.strip()

    if samples.empty:
        return False

    date_pattern = (
        r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}$"
        r"|^\d{1,2}[-/]\d{1,2}[-/]\d{2,4}$"
    )

    matches = samples.str.match(date_pattern)

    return matches.mean() >= 0.8


def infer_column_type(column_name, series):
    """Automatically infer a column's data type."""

    values = series.dropna()

    if len(values) == 0:
        return "text"

    if (
        column_name == "id"
        or column_name.endswith("_id")
        or column_name.endswith("_code")
    ):
        return "identifier"

    normalized = values.astype(str).str.strip().str.lower()

    boolean_values = {"true", "false", "yes", "no", "y", "n"}

    if normalized.isin(boolean_values).all():
        return "boolean"

    date_keywords = ("date", "time", "timestamp")

    if (
        any(keyword in column_name for keyword in date_keywords)
        or looks_like_date(values)
    ):
        parsed_dates = pd.to_datetime(
            values,
            format="mixed",
            errors="coerce"
        )

        if parsed_dates.notna().mean() >= 0.8:
            return "date"

    numeric_values = pd.to_numeric(values, errors="coerce")

    if numeric_values.notna().mean() >= 0.8:
        return "numeric"

    return "text"


def detect_schema(df):
    """Standardize columns and generate an automatic schema report."""

    df = standardize_column_names(df)

    schema = {}

    for column in df.columns:
        schema[column] = {
            "data_type": infer_column_type(column, df[column]),
            "total_records": int(len(df)),
            "non_null_count": int(df[column].notna().sum()),
            "null_count": int(df[column].isna().sum()),
            "unique_count": int(df[column].nunique()),
            "sample_values": (
                df[column].dropna().head(3).astype(str).tolist()
            )
        }

    return df, schema
