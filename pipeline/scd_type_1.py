import pandas as pd
from pathlib import Path

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SILVER_FOLDER = BASE_DIR / "data" / "silver"
GOLD_FOLDER = BASE_DIR / "data" / "gold"

SOURCE_FILE = SILVER_FOLDER / "sellers_json.parquet"
TARGET_FILE = GOLD_FOLDER / "dim_sellers.parquet"

BUSINESS_KEY = "seller_id"

# =====================================================
# Start
# =====================================================

print("=" * 60)
print("SCD TYPE 1 STARTED")
print("=" * 60)

print("Source File :", SOURCE_FILE)
print("Target File :", TARGET_FILE)

# =====================================================
# Check Source
# =====================================================

if not SOURCE_FILE.exists():
    raise FileNotFoundError(f"Source file not found:\n{SOURCE_FILE}")

# =====================================================
# Read Source
# =====================================================

source_df = pd.read_parquet(SOURCE_FILE)

print(f"Source Records : {len(source_df)}")

# =====================================================
# Create Gold Folder
# =====================================================

GOLD_FOLDER.mkdir(parents=True, exist_ok=True)

# =====================================================
# First Load
# =====================================================

if not TARGET_FILE.exists():

    print("\nNo existing Gold Dimension found.")
    print("Creating Initial Seller Dimension...\n")

    source_df.to_parquet(
        TARGET_FILE,
        index=False
    )

    print("✓ Seller Dimension Created")
    print(f"Rows Loaded : {len(source_df)}")

# =====================================================
# Incremental Load
# =====================================================

else:

    print("\nExisting Gold Dimension Found.\n")

    target_df = pd.read_parquet(TARGET_FILE)

    print(f"Existing Rows : {len(target_df)}")

    target_df = target_df.set_index(BUSINESS_KEY)
    source_df = source_df.set_index(BUSINESS_KEY)

    # Update existing records
    target_df.update(source_df)

    # Insert new records
    new_rows = source_df.loc[
        ~source_df.index.isin(target_df.index)
    ]

    target_df = pd.concat([target_df, new_rows])

    target_df.reset_index(inplace=True)

    target_df.to_parquet(
        TARGET_FILE,
        index=False
    )

    print("✓ Seller Dimension Updated")
    print(f"Rows Loaded : {len(target_df)}")

# =====================================================
# Completed
# =====================================================

print("\n" + "=" * 60)
print("SCD TYPE 1 COMPLETED")
print("=" * 60)