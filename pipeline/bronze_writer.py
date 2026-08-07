from pathlib import Path
from datetime import datetime
import uuid


def save_to_bronze(df, source_name, source_type):
    """
    Save DataFrame to Bronze Layer with metadata.
    """

    BASE_DIR = Path(__file__).resolve().parent.parent

    bronze_folder = BASE_DIR / "data" / "bronze"

    bronze_folder.mkdir(parents=True, exist_ok=True)

    # --------------------------
    # Metadata
    # --------------------------

    df["source_name"] = source_name

    df["source_type"] = source_type

    df["ingestion_timestamp"] = datetime.now()

    df["batch_id"] = str(uuid.uuid4())

    # --------------------------

    output_file = bronze_folder / f"{source_name}.parquet"

    df.to_parquet(output_file, index=False)

    print(f"✓ Saved {source_name} to Bronze Layer")