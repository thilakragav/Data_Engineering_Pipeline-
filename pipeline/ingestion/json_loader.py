import pandas as pd

def load_json(file_path):
    """
    Load a JSON file and return a DataFrame.
    """
    return pd.read_json(file_path)