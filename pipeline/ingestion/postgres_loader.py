import pandas as pd
from sqlalchemy import create_engine

def load_postgres(query, connection_string):
    """
    Execute a SQL query and return a DataFrame.
    """
    engine = create_engine(connection_string)
    return pd.read_sql(query, engine)