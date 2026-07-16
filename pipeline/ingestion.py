import os
from pathlib import Path
from datetime import datetime

import pandas as pd


# -----------------------------
# Project Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
BRONZE_FOLDER = PROJECT_ROOT / "data" / "bronze"

# Create Bronze folder if it doesn't exist
BRONZE_FOLDER.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Ingestion Function
# -----------------------------
def ingest_csv_to_bronze():

    csv_files = list(RAW_FOLDER.glob("*.csv"))

    if not csv_files:
        print("No CSV files found.")
        return

    print(f"\nFound {len(csv_files)} CSV files.\n")

    for file in csv_files:

        print(f"Reading : {file.name}")

        df = pd.read_csv(file)

        # Metadata
        df["load_timestamp"] = datetime.now()
        df["source_file"] = file.name

        parquet_name = file.stem + ".parquet"

        output_path = BRONZE_FOLDER / parquet_name

        df.to_parquet(output_path, index=False)

        print(f"Written : {output_path.name}")
        print(f"Rows    : {len(df)}")
        print("-" * 50)


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    ingest_csv_to_bronze()