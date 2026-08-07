from pathlib import Path
import pandas as pd

# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
STAGING_FOLDER = PROJECT_ROOT / "data" / "staging"

STAGING_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Creating Staging Layer")
print("=" * 60)

# =====================================================
# Read all files recursively
# =====================================================

for file in RAW_FOLDER.rglob("*"):

    if file.is_dir():
        continue

    print(f"\nProcessing : {file.relative_to(RAW_FOLDER)}")

    try:
        # -------------------------------
        # Read different file formats
        # -------------------------------

        if file.suffix.lower() == ".csv":
            df = pd.read_csv(file)

        elif file.suffix.lower() == ".json":
            df = pd.read_json(file)

        elif file.suffix.lower() == ".xml":
            df = pd.read_xml(file)

        elif file.suffix.lower() == ".parquet":
            df = pd.read_parquet(file)

        else:
            print(f"Skipping unsupported file : {file.name}")
            continue

        # -------------------------------
        # Standardize column names
        # -------------------------------

        df.columns = (
            df.columns
              .str.strip()
              .str.lower()
              .str.replace(" ", "_")
        )

        # -------------------------------
        # Remove empty rows
        # -------------------------------

        df = df.dropna(how="all")

        # -------------------------------
        # Remove duplicate rows
        # -------------------------------

        df = df.drop_duplicates()

        # -------------------------------
        # Trim spaces in string columns
        # -------------------------------

        object_columns = df.select_dtypes(include="object").columns

        for col in object_columns:
            df[col] = df[col].str.strip()

        # -------------------------------
        # Save as Parquet
        # -------------------------------

        output_file = STAGING_FOLDER / f"{file.stem}.parquet"

        df.to_parquet(
            output_file,
            index=False
        )

        print(f"✓ Saved : {output_file.name}")
        print(f"Rows    : {len(df)}")

    except Exception as e:
        print(f"✗ Error processing {file.name}")
        print(e)

print("\n" + "=" * 60)
print("Staging Layer Completed Successfully")
print("=" * 60)