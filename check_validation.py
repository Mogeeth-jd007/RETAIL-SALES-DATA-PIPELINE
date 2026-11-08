
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

processed_dir = BASE_DIR / "data" / "processed"
rejected_dir = BASE_DIR / "data" / "rejected"

files = {
    "Valid records": processed_dir / "valid_records.csv",
    "Warning records": processed_dir / "warning_records.csv",
    "Rejected records": rejected_dir / "rejected_records.csv"
}

print("\n========== VALIDATION FILE VERIFICATION ==========\n")

for name, file_path in files.items():

    if file_path.exists():

        df = pd.read_csv(file_path)

        print(f"{name}: {len(df)} records")
        print(df[["order_id", "status"]])

    else:
        print(f"{name}: FILE NOT FOUND!")

print("\n========== VERIFICATION COMPLETED ==========")
