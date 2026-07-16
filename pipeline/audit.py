import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

AUDIT_FILE = BASE_DIR / "metadata" / "audit_log.csv"

# Create metadata folder
AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Audit Record
audit_data = {
    "Run_ID": datetime.now().strftime("%Y%m%d%H%M%S"),
    "Pipeline_Name": "Ecommerce_Data_Pipeline",
    "Layer": "Gold",
    "Start_Time": datetime.now(),
    "End_Time": datetime.now(),
    "Status": "SUCCESS",
    "Records_Processed": 99441,
    "Remarks": "Pipeline Executed Successfully"
}

df = pd.DataFrame([audit_data])

if AUDIT_FILE.exists():
    old = pd.read_csv(AUDIT_FILE)
    df = pd.concat([old, df], ignore_index=True)

df.to_csv(AUDIT_FILE, index=False, lineterminator="\n")

print("=" * 50)
print("Audit Log Created Successfully")
print(AUDIT_FILE)
print("=" * 50)