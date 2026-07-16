import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from airflow.config.config import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:

        result = conn.execute(text("SELECT current_database();"))

        print("=" * 50)
        print("Connection Successful")
        print("=" * 50)

        print("Connected Database :", result.scalar())

except Exception as e:

    print("=" * 50)
    print("Connection Failed")
    print("=" * 50)

    print(e)
