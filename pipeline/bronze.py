from pathlib import Path
from datetime import datetime
import pandas as pd

# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STAGING_FOLDER = PROJECT_ROOT / "data" / "staging"
BRONZE_FOLDER = PROJECT_ROOT / "data" / "bronze"

BRONZE_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Creating Bronze Layer")
print("=" * 60)

parquet_files = list(STAGING_FOLDER.glob("*.parquet"))

if not parquet_files:
    print("No files found in Staging Layer.")
    exit()

batch_id = datetime.now().strftime("%Y%m%d%H%M%S")

for file in parquet_files:

    print(f"\nProcessing : {file.name}")

    df = pd.read_parquet(file)

    # ------------------------------------------
    # Bronze Metadata
    # ------------------------------------------

    df["ingestion_timestamp"] = datetime.now()
    df["batch_id"] = batch_id
    df["source_file"] = file.name
    df["record_status"] = "RAW"

    # ------------------------------------------
    # Save to Bronze
    # ------------------------------------------

    output_file = BRONZE_FOLDER / file.name

    df.to_parquet(
        output_file,
        index=False
    )

    print(f"Rows Loaded : {len(df)}")
    print(f"Saved To    : {output_file.name}")

print("\n" + "=" * 60)
print("Bronze Layer Created Successfully")
print("=" * 60)