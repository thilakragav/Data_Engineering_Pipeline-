import pandas as pd
from pathlib import Path

# --------------------------------------------------
# File Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_FILE = BASE_DIR / "data" / "silver" / "olist_sellers_dataset.parquet"
TARGET_FILE = BASE_DIR / "data" / "gold" / "dim_sellers_scd2.parquet"

BUSINESS_KEY = "seller_id"

# --------------------------------------------------
# Load Source Data
# --------------------------------------------------

print("=" * 60)
print("SCD TYPE 2 STARTED")
print("=" * 60)

source_df = pd.read_parquet(SOURCE_FILE)

today = pd.Timestamp.today().normalize()

# --------------------------------------------------
# First Load
# --------------------------------------------------

if not TARGET_FILE.exists():

    source_df["effective_date"] = today
    source_df["end_date"] = pd.NaT
    source_df["is_current"] = True
    source_df["version"] = 1

    TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    source_df.to_parquet(TARGET_FILE, index=False)

    print("Initial SCD Type 2 Dimension Created")
    print("Rows Loaded :", len(source_df))
    print("Saved To :", TARGET_FILE)

    exit()

# --------------------------------------------------
# Read Existing Gold Table
# --------------------------------------------------

target_df = pd.read_parquet(TARGET_FILE)

# --------------------------------------------------
# Process Each Customer
# --------------------------------------------------

for _, source_row in source_df.iterrows():

    customer_id = source_row[BUSINESS_KEY]

    current_record = target_df[
        (target_df[BUSINESS_KEY] == customer_id) &
        (target_df["is_current"] == True)
    ]

    # -----------------------------------------
    # New Customer
    # -----------------------------------------

    if current_record.empty:

        new_record = source_row.to_dict()

        new_record["effective_date"] = today
        new_record["end_date"] = pd.NaT
        new_record["is_current"] = True
        new_record["version"] = 1

        target_df = pd.concat(
            [target_df, pd.DataFrame([new_record])],
            ignore_index=True
        )

        continue

    # -----------------------------------------
    # Existing Customer
    # -----------------------------------------

    existing = current_record.iloc[0]

    changed = False

    compare_columns = [
        col for col in source_df.columns
        if col != BUSINESS_KEY
    ]

    for col in compare_columns:

        old = existing[col]
        new = source_row[col]

        if pd.isna(old) and pd.isna(new):
            continue

        if old != new:
            changed = True
            break

    if changed:

        idx = current_record.index[0]

        # Close old record

        target_df.loc[idx, "is_current"] = False
        target_df.loc[idx, "end_date"] = today

        # Insert new version

        new_record = source_row.to_dict()

        new_record["effective_date"] = today
        new_record["end_date"] = pd.NaT
        new_record["is_current"] = True
        new_record["version"] = int(existing["version"]) + 1

        target_df = pd.concat(
            [target_df, pd.DataFrame([new_record])],
            ignore_index=True
        )

# --------------------------------------------------
# Save
# --------------------------------------------------

target_df.to_parquet(TARGET_FILE, index=False)

print("=" * 60)
print("SCD TYPE 2 COMPLETED")
print("=" * 60)
print("Rows :", len(target_df))
print("Saved To :", TARGET_FILE)