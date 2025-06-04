# etl/load.py

from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

def load_data(df):
    print("💾 Loading data into PostgreSQL database...")

    # Exit early if DataFrame is empty or None
    if df is None or df.empty:
        print("⚠️ No data to load.")
        return

    # Load environment variables from .env file
    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    # Create SQLAlchemy engine for PostgreSQL connection
    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    # Load the DataFrame into the "anime" table (replace if exists)
    df.to_sql("anime", con=engine, if_exists="replace", index=False, method='multi')

    print("✅ Data successfully loaded into PostgreSQL database: anime_db")
