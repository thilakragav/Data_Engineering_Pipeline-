"""
ingestion_manager.py

This module acts as the central controller for all data ingestion.
It routes the request to the appropriate loader based on the source type.
"""

from pipeline.ingestion.csv_loader import load_csv
from pipeline.ingestion.json_loader import load_json
from pipeline.ingestion.xml_loader import load_xml
from pipeline.ingestion.postgres_loader import load_postgres


def load_data(source_type, **kwargs):
    """
    Load data from different source types.

    Parameters
    ----------
    source_type : str
        Type of data source.
        Supported values:
            - csv
            - json
            - xml
            - postgres

    kwargs : dict
        Additional parameters required by each loader.

    Returns
    -------
    pandas.DataFrame
        Loaded data.
    """

    source_type = source_type.lower()

    if source_type == "csv":
        return load_csv(kwargs["path"])

    elif source_type == "json":
        return load_json(kwargs["path"])

    elif source_type == "xml":
        return load_xml(kwargs["path"])

    elif source_type == "postgres":
        return load_postgres(
            query=kwargs["query"],
            connection_string=kwargs["connection_string"]
        )

    else:
        raise ValueError(
            f"Unsupported source type: {source_type}"
        )


# --------------------------------------------------------
# Test the ingestion manager
# --------------------------------------------------------

if __name__ == "__main__":

    # ---------- CSV ----------
    print("\nLoading CSV...")

    csv_df = load_data(
        source_type="csv",
        path="data/raw/csv/olist_customers_dataset.csv"
    )

    print(csv_df.head())

    # ---------- JSON ----------
    print("\nLoading JSON...")

    json_df = load_data(
        source_type="json",
        path="data/raw/json/olist_customers_dataset.json"
    )

    print(json_df.head())

    # ---------- XML ----------
    print("\nLoading XML...")

    xml_df = load_data(
        source_type="xml",
        path="data/raw/xml/olist_products_dataset.xml"
    )

    print(xml_df.head())

    # ---------- PostgreSQL ----------
    # Uncomment after PostgreSQL is configured.

    """
    postgres_df = load_data(
        source_type="postgres",
        query="SELECT * FROM customers",
        connection_string="postgresql://postgres:password@localhost:5432/olist"
    )

    print(postgres_df.head())
    """