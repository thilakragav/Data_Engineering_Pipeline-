import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import pandas as pd
from config import engine

# Gold folder
BASE_DIR = Path(__file__).resolve().parent.parent
GOLD_FOLDER = BASE_DIR / "data" / "gold"

gold_files = [
    "fact_sales.parquet",
    "dim_customers.parquet",
    "dim_products.parquet",
    "dim_sellers.parquet",
    "monthly_sales.parquet",
    "sales_by_state.parquet",
    "customer_summary.parquet",
    "top_products.parquet"
]

print("=" * 60)
print("Loading Gold Layer into PostgreSQL")
print("=" * 60)

for file in gold_files:

    file_path = GOLD_FOLDER / file

    if not file_path.exists():
        print(f"Skipping {file} (Not Found)")
        continue

    table_name = file.replace(".parquet", "")

    df = pd.read_parquet(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded: {table_name}")

print("=" * 60)
print("Gold Layer Loaded Successfully")
print("=" * 60)