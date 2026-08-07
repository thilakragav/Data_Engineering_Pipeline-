import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

csv_folder = BASE_DIR / "data" / "raw" / "csv"
json_folder = BASE_DIR / "data" / "raw" / "json"

json_folder.mkdir(exist_ok=True)

files = [
    "olist_customers_dataset",
    "olist_order_reviews_dataset",
    "olist_sellers_dataset"
]

for file in files:
    df = pd.read_csv(csv_folder / f"{file}.csv")

    df.to_json(
        json_folder / f"{file}.json",
        orient="records",
        indent=4
    )

    print(f"Converted {file}.csv -> {file}.json")

print("Done!")