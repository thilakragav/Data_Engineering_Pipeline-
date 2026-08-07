import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

csv_file = BASE_DIR / "data" / "raw" / "csv" / "product_category_name_translation.csv"

xml_file = BASE_DIR / "data" / "raw" / "xml" / "product_category_name_translation.xml"

df = pd.read_csv(csv_file)

df.to_xml(
    xml_file,
    index=False,
    root_name="products",
    row_name="product"
)

print("XML file created successfully.")