import pandas as pd
from pathlib import Path

from pipeline.db_config import engine

BASE_DIR = Path(__file__).resolve().parent.parent
GOLD_FOLDER = BASE_DIR / "data" / "gold"

gold_files = [
    "fact_sales.parquet",
    "dim_customers.parquet",
    "dim_customers_scd2.parquet",
    "dim_products.parquet",
    "dim_sellers.parquet",
    "dim_sellers_scd2.parquet",
    "monthly_sales.parquet",
    "sales_by_state.parquet",
    "customer_summary.parquet",
    "top_products.parquet",
]

print("=" * 60)
print("Loading Gold Layer into PostgreSQL")
print("=" * 60)

loaded_tables = 0

for file in gold_files:
    file_path = GOLD_FOLDER / file

    if not file_path.exists():
        print(f"Skipping {file} (File Not Found)")
        continue

    table_name = file.replace(".parquet", "")

    print(f"Loading {table_name}...")

    df = pd.read_parquet(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
    )

    print(f"Loaded {table_name} ({len(df)} rows)")
    loaded_tables += 1

print("=" * 60)
print("Gold Layer Loaded Successfully")
print("=" * 60)
print(f"Tables Loaded: {loaded_tables}")