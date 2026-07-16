from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql+psycopg2://postgres:Thilak%402005@ecommerce_postgres:5432/ecommerce_dw"
)

engine = create_engine(DATABASE_URL)