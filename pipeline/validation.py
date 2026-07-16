from pathlib import Path
import pandas as pd

# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BRONZE_FOLDER = PROJECT_ROOT / "data" / "bronze"
SILVER_FOLDER = PROJECT_ROOT / "data" / "silver"
REJECT_FOLDER = PROJECT_ROOT / "data" / "reject"

SILVER_FOLDER.mkdir(parents=True, exist_ok=True)
REJECT_FOLDER.mkdir(parents=True, exist_ok=True)

# =====================================================
# Validation Rules
# =====================================================

VALIDATION_RULES = {

    "olist_customers_dataset": {
        "primary_key": ["customer_id"],
        "required_columns": ["customer_id", "customer_unique_id"]
    },

    "olist_orders_dataset": {
        "primary_key": ["order_id"],
        "required_columns": ["order_id", "customer_id"]
    },

    "olist_products_dataset": {
        "primary_key": ["product_id"],
        "required_columns": ["product_id"]
    },

    "olist_order_items_dataset": {
        "primary_key": ["order_id", "order_item_id"],
        "required_columns": ["order_id", "order_item_id", "product_id"]
    },

    "olist_order_payments_dataset": {
        "primary_key": ["order_id", "payment_sequential"],
        "required_columns": ["order_id", "payment_sequential"]
    },

    "olist_order_reviews_dataset": {
        "primary_key": ["review_id"],
        "required_columns": ["review_id", "order_id"]
    },

    "olist_sellers_dataset": {
        "primary_key": ["seller_id"],
        "required_columns": ["seller_id"]
    },

    "olist_geolocation_dataset": {
        "primary_key": [
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng"
        ],
        "required_columns": ["geolocation_zip_code_prefix"]
    },

    "product_category_name_translation": {
        "primary_key": ["product_category_name"],
        "required_columns": [
            "product_category_name",
            "product_category_name_english"
        ]
    }

}

# =====================================================
# Validation Function
# =====================================================

def validate_data():

    parquet_files = list(BRONZE_FOLDER.glob("*.parquet"))

    if len(parquet_files) == 0:
        print("No Parquet files found in Bronze Layer.")
        return

    print(f"\nFound {len(parquet_files)} files to validate.\n")

    for file in parquet_files:

        dataset_name = file.stem

        print("=" * 60)
        print(f"Validating : {dataset_name}")

        if dataset_name not in VALIDATION_RULES:
            print("Validation rules not available.")
            continue

        rules = VALIDATION_RULES[dataset_name]

        df = pd.read_parquet(file)

        total_records = len(df)

        # ------------------------------------------
        # NULL CHECK
        # ------------------------------------------

        valid_df = df.dropna(subset=rules["required_columns"])

        reject_df = df.loc[
            ~df.index.isin(valid_df.index)
        ].copy()

        # ------------------------------------------
        # DUPLICATE CHECK
        # ------------------------------------------

        duplicate_rows = valid_df[
            valid_df.duplicated(
                subset=rules["primary_key"],
                keep="first"
            )
        ]

        valid_df = valid_df.drop_duplicates(
            subset=rules["primary_key"],
            keep="first"
        )

        reject_df = pd.concat(
            [reject_df, duplicate_rows],
            ignore_index=True
        )

        # ------------------------------------------
        # SAVE FILES
        # ------------------------------------------

        silver_file = SILVER_FOLDER / file.name
        reject_file = REJECT_FOLDER / file.name

        valid_df.to_parquet(
            silver_file,
            index=False
        )

        reject_df.to_parquet(
            reject_file,
            index=False
        )

        # ------------------------------------------
        # SUMMARY
        # ------------------------------------------

        print(f"Total Records     : {total_records}")
        print(f"Valid Records     : {len(valid_df)}")
        print(f"Rejected Records  : {len(reject_df)}")
        print("Saved to Silver   :", silver_file.name)
        print("Saved to Reject   :", reject_file.name)

    print("\nValidation Completed Successfully.")


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":
    validate_data()