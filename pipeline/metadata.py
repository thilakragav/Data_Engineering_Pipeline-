import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_FILE = BASE_DIR / "data" / "gold" / "fact_sales.parquet"

METADATA_FILE = BASE_DIR / "metadata" / "metadata_log.csv"

METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(SOURCE_FILE)

metadata = {
    "Dataset_Name": "fact_sales",
    "Rows": len(df),
    "Columns": len(df.columns),
    "Column_Names": " | ".join(df.columns),
    "File_Type": "Parquet",
    "Created_On": datetime.now()
}

meta_df = pd.DataFrame([metadata])

if METADATA_FILE.exists():
    old = pd.read_csv(METADATA_FILE)
    meta_df = pd.concat([old, meta_df], ignore_index=True)

meta_df.to_csv(METADATA_FILE, index=False, lineterminator="\n")

print("=" * 50)
print("Metadata File Created Successfully")
print(METADATA_FILE)
print("=" * 50)