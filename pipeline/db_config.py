from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://postgres:password@eco:5432/ece_db"
)

engine = create_engine(DATABASE_URL)
