from pipeline.config_loader import load_config
from pipeline.ingestion.ingestion_manager import load_data
from pipeline.bronze_writer import save_to_bronze


def run_ingestion():
    """
    Read all configured sources and save them to the Bronze layer.
    """

    config = load_config("sources.yaml")

    sources = config["sources"]

    for source_name, source in sources.items():

        print(f"\nProcessing : {source_name}")

        source_type = source["type"]

        try:

            if source_type in ["csv", "json", "xml"]:

                df = load_data(
                    source_type=source_type,
                    path=source["path"]
                )

            elif source_type == "postgres":

                df = load_data(
                    source_type="postgres",
                    query=source["query"],
                    connection_string=source["connection_string"]
                )

            else:

                raise ValueError(
                    f"Unsupported source type : {source_type}"
                )

            save_to_bronze(
    df,
    source_name,
    source_type
)

            print(f"✓ {source_name} completed successfully.")

        except Exception as e:

            print(f"✗ Error processing {source_name}")
            print(e)


if __name__ == "__main__":
    run_ingestion()