import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE = BASE_DIR / "data" / "transformed" / "master_sales.parquet"
GOLD = BASE_DIR / "data" / "gold"

GOLD.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("(3/3) Creating Gold Layer")
print("=" * 60)

df = pd.read_parquet(SOURCE)

# --------------------------------------------------
# FACT SALES
# --------------------------------------------------

fact_sales = df.copy()

fact_sales.to_parquet(
    GOLD / "fact_sales.parquet",
    index=False
)

print("✓ fact_sales.parquet created")

# --------------------------------------------------
# CUSTOMER DIMENSION
# --------------------------------------------------

customer_dim = df[
    [
        "customer_id",
        "customer_unique_id",
        "customer_city",
        "customer_state"
    ]
].drop_duplicates()

customer_dim.to_parquet(
    GOLD / "dim_customers.parquet",
    index=False
)

print("✓ dim_customers.parquet created")

# --------------------------------------------------
# PRODUCT DIMENSION
# --------------------------------------------------

product_dim = df[
    [
        "product_id",
        "product_category_name",
        "product_weight_g"
    ]
].drop_duplicates()

product_dim.to_parquet(
    GOLD / "dim_products.parquet",
    index=False
)

print("✓ dim_products.parquet created")

# --------------------------------------------------
# SELLER DIMENSION
# --------------------------------------------------

seller_dim = df[
    [
        "seller_id",
        "seller_city",
        "seller_state"
    ]
].drop_duplicates()

seller_dim.to_parquet(
    GOLD / "dim_sellers.parquet",
    index=False
)

print("✓ dim_sellers.parquet created")

# --------------------------------------------------
# MONTHLY SALES
# --------------------------------------------------

df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

monthly_sales = (
    df.groupby("month")["payment_value"]
      .sum()
      .reset_index()
)

monthly_sales.to_parquet(
    GOLD / "monthly_sales.parquet",
    index=False
)

print("✓ monthly_sales.parquet created")

# --------------------------------------------------
# SALES BY STATE
# --------------------------------------------------

sales_state = (
    df.groupby("customer_state")["payment_value"]
      .sum()
      .reset_index()
)

sales_state.to_parquet(
    GOLD / "sales_by_state.parquet",
    index=False
)

print("✓ sales_by_state.parquet created")

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

top_products = (
    df.groupby("product_category_name")
      .agg(
          Total_Sales=("payment_value", "sum"),
          Orders=("order_id", "count")
      )
      .reset_index()
      .sort_values(
          "Total_Sales",
          ascending=False
      )
)

top_products.to_parquet(
    GOLD / "top_products.parquet",
    index=False
)

print("✓ top_products.parquet created")

# --------------------------------------------------
# CUSTOMER SUMMARY
# --------------------------------------------------

customer_summary = (
    df.groupby("customer_id")
      .agg(
          Total_Orders=("order_id", "count"),
          Total_Spent=("payment_value", "sum")
      )
      .reset_index()
)

customer_summary.to_parquet(
    GOLD / "customer_summary.parquet",
    index=False
)

print("✓ customer_summary.parquet created")

print("=" * 60)
print("(3/3) Gold Layer Created Successfully")
print("=" * 60)