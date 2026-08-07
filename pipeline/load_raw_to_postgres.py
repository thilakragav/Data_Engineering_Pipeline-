import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# PostgreSQL connection
engine = create_engine(
    "postgresql://postgres:Thilak%402005@localhost:5432/olist"
)

# CSV files to load
files = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "payments": "olist_order_payments_dataset.csv"
}

for table_name, file_name in files.items():

    file_path = BASE_DIR / "data" / "raw" / "csv" / file_name

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"✓ Loaded {table_name}")

print("\nAll tables loaded successfully!")