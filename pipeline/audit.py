import pandas as pd
from pathlib import Path
from datetime import datetime

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

GOLD_FILE = BASE_DIR / "data" / "gold" / "fact_sales.parquet"

AUDIT_FOLDER = BASE_DIR / "metadata"
AUDIT_FOLDER.mkdir(parents=True, exist_ok=True)

AUDIT_FILE = AUDIT_FOLDER / "audit_log.csv"

# =====================================================
# Start Time
# =====================================================

start_time = datetime.now()

# =====================================================
# Read Gold Layer
# =====================================================

if not GOLD_FILE.exists():
    raise FileNotFoundError(f"Gold file not found:\n{GOLD_FILE}")

df = pd.read_parquet(GOLD_FILE)

# =====================================================
# End Time
# =====================================================

end_time = datetime.now()

duration = round((end_time - start_time).total_seconds(), 2)

# =====================================================
# Audit Record
# =====================================================

audit_record = {

    "Run_ID": start_time.strftime("%Y%m%d%H%M%S"),

    "Pipeline_Name": "Ecommerce_Data_Pipeline",

    "Layer": "Gold",

    "Start_Time": start_time,

    "End_Time": end_time,

    "Duration_Seconds": duration,

    "Status": "SUCCESS",

    "Records_Processed": len(df),

    "Remarks": "Gold Layer Loaded Successfully"

}

audit_df = pd.DataFrame([audit_record])

# =====================================================
# Append Existing Audit
# =====================================================

if AUDIT_FILE.exists():

    existing = pd.read_csv(AUDIT_FILE)

    audit_df = pd.concat(
        [existing, audit_df],
        ignore_index=True
    )

audit_df.to_csv(
    AUDIT_FILE,
    index=False
)

# =====================================================
# Completed
# =====================================================

print("=" * 60)
print("Audit Log Generated Successfully")
print("=" * 60)
print(f"Pipeline : {audit_record['Pipeline_Name']}")
print(f"Layer    : {audit_record['Layer']}")
print(f"Records  : {audit_record['Records_Processed']}")
print(f"Duration : {audit_record['Duration_Seconds']} sec")
print(f"Saved    : {AUDIT_FILE}")
print("=" * 60)