import pandas as pd
from pathlib import Path

# -----------------------------------
# File Paths
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_FILE = BASE_DIR / "data" / "silver" / "olist_sellers_dataset.parquet"
TARGET_FILE = BASE_DIR / "data" / "gold" / "dim_sellers.parquet"

BUSINESS_KEY = "seller_id"

# -----------------------------------
# Check Source File
# -----------------------------------
print("=" * 60)
print("SCD TYPE 1 STARTED")
print("=" * 60)

print("Source File :", SOURCE_FILE)
print("Target File :", TARGET_FILE)

if not SOURCE_FILE.exists():
    raise FileNotFoundError(f"Source file not found:\n{SOURCE_FILE}")

# -----------------------------------
# Read Source Data
# -----------------------------------
source_df = pd.read_parquet(SOURCE_FILE)

print(f"Source Records : {len(source_df)}")

# -----------------------------------
# Create Gold Folder
# -----------------------------------
TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------------
# First Load
# -----------------------------------
if not TARGET_FILE.exists():

    print("Gold table does not exist.")
    print("Creating Initial Dimension Table...")

    source_df.to_parquet(TARGET_FILE, index=False)

    print("Dimension table created successfully.")
    print("Rows Loaded :", len(source_df))

else:

    print("Existing Gold table found.")

    target_df = pd.read_parquet(TARGET_FILE)

    print("Existing Rows :", len(target_df))

    # Merge source and target
    merged = target_df.set_index(BUSINESS_KEY)

    source = source_df.set_index(BUSINESS_KEY)

    # Update existing rows
    merged.update(source)

    # Insert new rows
    new_rows = source.loc[~source.index.isin(merged.index)]

    merged = pd.concat([merged, new_rows])

    merged.reset_index(inplace=True)

    merged.to_parquet(TARGET_FILE, index=False)

    print("Dimension Updated Successfully.")
    print("Rows Loaded :", len(merged))

print("=" * 60)
print("SCD TYPE 1 COMPLETED")
print("=" * 60)