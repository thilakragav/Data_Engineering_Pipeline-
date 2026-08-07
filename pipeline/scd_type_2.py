import pandas as pd
from pathlib import Path

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SILVER_FOLDER = BASE_DIR / "data" / "silver"
GOLD_FOLDER = BASE_DIR / "data" / "gold"

SOURCE_FILE = SILVER_FOLDER / "customers_csv.parquet"
TARGET_FILE = GOLD_FOLDER / "dim_customers_scd2.parquet"

BUSINESS_KEY = "customer_id"

# =====================================================
# Start
# =====================================================

print("=" * 60)
print("SCD TYPE 2 STARTED")
print("=" * 60)

print("Source :", SOURCE_FILE)
print("Target :", TARGET_FILE)

if not SOURCE_FILE.exists():
    raise FileNotFoundError(f"Source file not found:\n{SOURCE_FILE}")

source_df = pd.read_parquet(SOURCE_FILE)

today = pd.Timestamp.today().normalize()

# =====================================================
# First Load
# =====================================================

if not TARGET_FILE.exists():

    source_df["effective_date"] = today
    source_df["end_date"] = pd.NaT
    source_df["is_current"] = True
    source_df["version"] = 1

    GOLD_FOLDER.mkdir(parents=True, exist_ok=True)

    source_df.to_parquet(
        TARGET_FILE,
        index=False
    )

    print("✓ Initial Customer Dimension Created")
    print(f"Rows Loaded : {len(source_df)}")
    print("=" * 60)
    exit()

# =====================================================
# Existing Gold Table
# =====================================================

target_df = pd.read_parquet(TARGET_FILE)

# =====================================================
# Process Records
# =====================================================

for _, source_row in source_df.iterrows():

    business_id = source_row[BUSINESS_KEY]

    current_record = target_df[
        (target_df[BUSINESS_KEY] == business_id)
        &
        (target_df["is_current"] == True)
    ]

    # ---------------------------------------
    # New Record
    # ---------------------------------------

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

    # ---------------------------------------
    # Existing Record
    # ---------------------------------------

    existing = current_record.iloc[0]

    compare_columns = [

        col

        for col in source_df.columns

        if col != BUSINESS_KEY

    ]

    changed = False

    for col in compare_columns:

        old = existing[col]
        new = source_row[col]

        if pd.isna(old) and pd.isna(new):
            continue

        if old != new:
            changed = True
            break

    # ---------------------------------------
    # New Version
    # ---------------------------------------

    if changed:

        idx = current_record.index[0]

        target_df.loc[idx, "is_current"] = False
        target_df.loc[idx, "end_date"] = today

        new_record = source_row.to_dict()

        new_record["effective_date"] = today
        new_record["end_date"] = pd.NaT
        new_record["is_current"] = True
        new_record["version"] = int(existing["version"]) + 1

        target_df = pd.concat(
            [target_df, pd.DataFrame([new_record])],
            ignore_index=True
        )

# =====================================================
# Save
# =====================================================

target_df.to_parquet(
    TARGET_FILE,
    index=False
)

print("=" * 60)
print("SCD TYPE 2 COMPLETED")
print("=" * 60)

print(f"Rows : {len(target_df)}")
print(f"Saved : {TARGET_FILE}")