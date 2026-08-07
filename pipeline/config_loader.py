from pathlib import Path
import yaml

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Config folder
CONFIG_DIR = BASE_DIR / "config"


def load_config(config_file="sources.yaml"):
    """
    Load YAML configuration file from the config folder.
    """

    config_path = CONFIG_DIR / config_file

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config


if __name__ == "__main__":
    config = load_config()
    print(config)