import pandas as pd

def load_xml(file_path):
    """
    Load an XML file and return a DataFrame.
    """
    return pd.read_xml(file_path)