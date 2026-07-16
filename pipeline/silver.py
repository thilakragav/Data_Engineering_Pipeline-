from pathlib import Path
import pandas as pd

# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SILVER_FOLDER = PROJECT_ROOT / "data" / "silver"

# =====================================================
# Cleaning Function
# =====================================================

def clean_dataframe(df):

    # -----------------------------
    # Trim spaces from text columns
    # -----------------------------
    object_columns = df.select_dtypes(include="object").columns

    for col in object_columns:
        df[col] = df[col].str.strip()

    # -----------------------------
    # Standardize city names
    # -----------------------------
    if "customer_city" in df.columns:
        df["customer_city"] = df["customer_city"].str.title()

    if "seller_city" in df.columns:
        df["seller_city"] = df["seller_city"].str.title()

    # -----------------------------
    # Standardize state codes
    # -----------------------------
    if "customer_state" in df.columns:
        df["customer_state"] = df["customer_state"].str.upper()

    if "seller_state" in df.columns:
        df["seller_state"] = df["seller_state"].str.upper()

    # -----------------------------
    # Convert date columns
    # -----------------------------
    for column in df.columns:

        if "timestamp" in column or "date" in column:

            try:
                df[column] = pd.to_datetime(df[column])

            except Exception:
                pass

    # -----------------------------
    # Convert numeric columns
    # -----------------------------
    numeric_columns = [
        "price",
        "freight_value",
        "payment_value",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # -----------------------------
    # Remove duplicate rows
    # -----------------------------
    df = df.drop_duplicates()

    return df


# =====================================================
# Silver Layer
# =====================================================

def silver_layer():

    parquet_files = list(SILVER_FOLDER.glob("*.parquet"))

    if not parquet_files:
        print("No validated files found.")
        return

    print(f"\nCleaning {len(parquet_files)} datasets...\n")

    for file in parquet_files:

        print("=" * 60)
        print(f"Processing : {file.name}")

        df = pd.read_parquet(file)

        before = len(df)

        df = clean_dataframe(df)

        after = len(df)

        df.to_parquet(file, index=False)

        print(f"Rows Before : {before}")
        print(f"Rows After  : {after}")
        print("Cleaning Completed")

    print("\n(2/3) Silver Layer Completed Successfully.")


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":
    silver_layer()