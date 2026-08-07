from pathlib import Path
from unicodedata import name
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SILVER_FOLDER = PROJECT_ROOT / "data" / "silver"
TRANSFORMED_FOLDER = PROJECT_ROOT / "data" / "transformed"

TRANSFORMED_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Load Data
# ==========================================================

def load_data():

    print("\nLoading Silver Layer Files...\n")

    datasets = {

        "customers": pd.read_parquet(
            SILVER_FOLDER / "customers_csv.parquet"
        ),

        "orders": pd.read_parquet(
            SILVER_FOLDER / "orders_csv.parquet"
        ),

        "order_items": pd.read_parquet(
            SILVER_FOLDER / "order_items_csv.parquet"
        ),

        "products": pd.read_parquet(
            SILVER_FOLDER / "products_xml.parquet"
        ),

        "payments": pd.read_parquet(
            SILVER_FOLDER / "payments_csv.parquet"
        ),

        "reviews": pd.read_parquet(
            SILVER_FOLDER / "reviews_csv.parquet"
        ),

        "sellers": pd.read_parquet(
            SILVER_FOLDER / "sellers_json.parquet"
        ),

        "geolocation": pd.read_parquet(
            SILVER_FOLDER / "geolocation_csv.parquet"
        ),

        "category": pd.read_parquet(
            SILVER_FOLDER / "category_csv.parquet"
        )

    }

    print("✓ All datasets loaded successfully.\n")

    for name, df in datasets.items():
        print(f"\n{name}")
        print(df.columns.tolist())

    return datasets


# ==========================================================
# Prepare Data
# ==========================================================

def prepare_data(datasets):

    print("Preparing datasets...\n")

    # ------------------------------------------
    # Remove Metadata Columns
    # ------------------------------------------

    for name in datasets:

        datasets[name] = datasets[name].drop(
        columns=[
            "load_timestamp",
            "source_file",
            "batch_id",
            "source_name",
            "source_type",
            "ingestion_timestamp"
        ],
        errors="ignore"
    )

    print("✓ Metadata removed.")

    # ------------------------------------------
    # Aggregate Payments
    # One payment record per order
    # ------------------------------------------

    datasets["payments"] = (

        datasets["payments"]

        .groupby("order_id", as_index=False)

        .agg({

            "payment_value": "sum",

            "payment_type": "first",

            "payment_installments": "max"

        })

    )

    print("✓ Payments aggregated.")

    # ------------------------------------------
    # Remove Duplicate Reviews
    # ------------------------------------------

    datasets["reviews"] = (

        datasets["reviews"]

        .drop_duplicates(

            subset="order_id",

            keep="first"

        )

    )

    print("✓ Reviews prepared.")

    # ------------------------------------------
    # Geolocation Lookup
    # ------------------------------------------

    datasets["geolocation"] = (

        datasets["geolocation"]

        .drop_duplicates(

            subset="geolocation_zip_code_prefix",

            keep="first"

        )

    )

    print("✓ Geolocation prepared.\n")


# ==========================================================
# Join Tables
# ==========================================================

def join_tables(datasets):

    print("Joining datasets...\n")

    master = datasets["orders"]

    master = master.merge(

        datasets["customers"],

        on="customer_id",

        how="left"

    )

    master = master.merge(

        datasets["order_items"],

        on="order_id",

        how="left"

    )

    master = master.merge(

        datasets["products"],

        on="product_id",

        how="left"

    )

    master = master.merge(

        datasets["category"],

        on="product_category_name",

        how="left"

    )

    master = master.merge(

        datasets["payments"],

        on="order_id",

        how="left"

    )

    master = master.merge(

        datasets["reviews"],

        on="order_id",

        how="left"

    )

    master = master.merge(

        datasets["sellers"],

        on="seller_id",

        how="left",

        suffixes=("", "_seller")

    )

    print(f"✓ Joined Successfully : {master.shape}\n")

    return master
# ==========================================================
# Create Business Features
# ==========================================================

def create_features(master):

    print("Creating Business Features...\n")

    # ------------------------------------------
    # Convert Date Columns
    # ------------------------------------------

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "shipping_limit_date",
        "review_creation_date",
        "review_answer_timestamp"
    ]

    for col in date_columns:

        if col in master.columns:

            master[col] = pd.to_datetime(
                master[col],
                errors="coerce"
            )

    # ------------------------------------------
    # Total Amount
    # ------------------------------------------

    master["total_amount"] = (
        master["price"].fillna(0)
        + master["freight_value"].fillna(0)
    )

    # ------------------------------------------
    # Delivery Days
    # ------------------------------------------

    master["delivery_days"] = (
        master["order_delivered_customer_date"]
        - master["order_purchase_timestamp"]
    ).dt.days

    # ------------------------------------------
    # Order Year & Month
    # ------------------------------------------

    master["order_year"] = (
        master["order_purchase_timestamp"].dt.year
    )

    master["order_month"] = (
        master["order_purchase_timestamp"].dt.month_name()
    )

    # ------------------------------------------
    # Customer Location
    # ------------------------------------------

    master["customer_location"] = (
        master["customer_city"].fillna("")
        + ", "
        + master["customer_state"].fillna("")
    )

    # ------------------------------------------
    # Seller Location
    # ------------------------------------------

    master["seller_location"] = (
        master["seller_city"].fillna("")
        + ", "
        + master["seller_state"].fillna("")
    )

    # ------------------------------------------
    # Payment Status
    # ------------------------------------------

    master["payment_status"] = master["payment_value"].apply(
        lambda x: "Paid" if pd.notna(x) and x > 0 else "Unpaid"
    )

    # ------------------------------------------
    # Review Category
    # ------------------------------------------

    master["review_category"] = master["review_score"].map({
        5: "Excellent",
        4: "Good",
        3: "Average",
        2: "Poor",
        1: "Poor"
    }).fillna("No Review")

    # ------------------------------------------
    # Product Volume
    # ------------------------------------------

    master["product_volume_cm3"] = (
        master["product_length_cm"].fillna(0)
        * master["product_width_cm"].fillna(0)
        * master["product_height_cm"].fillna(0)
    )

    print("✓ Business Features Created.\n")

    return master


# ==========================================================
# Save Output
# ==========================================================

def save_output(master):

    output_file = (
        TRANSFORMED_FOLDER / "master_sales.parquet"
    )

    master.to_parquet(
        output_file,
        index=False
    )

    print(f"✓ Saved : {output_file.name}\n")


# ==========================================================
# Main Function
# ==========================================================

def main():

    print("=" * 60)
    print("Business Transformation Started")
    print("=" * 60)

    # Load Data
    datasets = load_data()

    # Prepare Data
    prepare_data(datasets)

    # Join Tables
    master = join_tables(datasets)

    # Business Features
    master = create_features(master)

    # Save Output
    save_output(master)

    print("=" * 60)
    print("Business Transformation Completed Successfully")
    print("=" * 60)
    print(f"Total Records : {len(master)}")


# ==========================================================
# Execute
# ==========================================================

if __name__ == "__main__":
    main()