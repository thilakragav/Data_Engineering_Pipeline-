import pandas as pd
from pathlib import Path
from datetime import datetime

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_FILE = BASE_DIR / "data" / "gold" / "fact_sales.parquet"

METADATA_FOLDER = BASE_DIR / "metadata"
METADATA_FOLDER.mkdir(parents=True, exist_ok=True)

METADATA_FILE = METADATA_FOLDER / "metadata_log.csv"

# =====================================================
# Check Source
# =====================================================

if not SOURCE_FILE.exists():
    raise FileNotFoundError(f"Source file not found:\n{SOURCE_FILE}")

# =====================================================
# Read Dataset
# =====================================================

df = pd.read_parquet(SOURCE_FILE)

# =====================================================
# Metadata Information
# =====================================================

metadata = {

    "Dataset_Name": "fact_sales",

    "Pipeline_Stage": "Gold",

    "Source_File": SOURCE_FILE.name,

    "File_Type": "Parquet",

    "Rows": len(df),

    "Columns": len(df.columns),

    "Column_Names": ", ".join(df.columns),

    "File_Size_MB": round(
        SOURCE_FILE.stat().st_size / (1024 * 1024),
        2
    ),

    "Load_Timestamp": datetime.now(),

    "Status": "Success"

}

meta_df = pd.DataFrame([metadata])

# =====================================================
# Append Metadata
# =====================================================

if METADATA_FILE.exists():

    existing = pd.read_csv(METADATA_FILE)

    meta_df = pd.concat(
        [existing, meta_df],
        ignore_index=True
    )

meta_df.to_csv(
    METADATA_FILE,
    index=False
)

# =====================================================
# Completed
# =====================================================

print("=" * 60)
print("Metadata Generated Successfully")
print("=" * 60)
print(f"Dataset : {metadata['Dataset_Name']}")
print(f"Rows    : {metadata['Rows']}")
print(f"Columns : {metadata['Columns']}")
print(f"Saved   : {METADATA_FILE}")
print("=" * 60)