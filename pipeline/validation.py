from pathlib import Path
import pandas as pd

# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BRONZE_FOLDER = PROJECT_ROOT / "data" / "bronze"
VALIDATED_FOLDER = PROJECT_ROOT / "data" / "validated"

VALIDATED_FOLDER.mkdir(parents=True, exist_ok=True)
REJECT_FOLDER = PROJECT_ROOT / "data" / "reject"

VALIDATED_FOLDER.mkdir(parents=True, exist_ok=True)
REJECT_FOLDER.mkdir(parents=True, exist_ok=True)

# =====================================================
# Validation Rules
# =====================================================

VALIDATION_RULES = {

"orders_csv": {
    "primary_key": ["order_id"],
    "required_columns": ["order_id", "customer_id"]
},

"order_items_csv": {
    "primary_key": ["order_id", "order_item_id"],
    "required_columns": ["order_id", "order_item_id", "product_id"]
},

"payments_csv": {
    "primary_key": ["order_id", "payment_sequential"],
    "required_columns": ["order_id", "payment_sequential"]
},

"reviews_csv": {
    "primary_key": ["review_id"],
    "required_columns": ["review_id", "order_id"]
},

"geolocation_csv": {
    "primary_key": [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng"
    ],
    "required_columns": [
        "geolocation_zip_code_prefix"
    ]
},

"category_csv": {
    "primary_key": [
        "product_category_name"
    ],
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

        validated_file = VALIDATED_FOLDER / file.name
        reject_file = REJECT_FOLDER / file.name

        valid_df.to_parquet(
            validated_file,
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
        print("Saved to Validated :", validated_file.name)
        print("Saved to Reject   :", reject_file.name)

    print("\nValidation Completed Successfully.")


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":
    validate_data()