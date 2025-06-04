# main.py

# Import ETL functions from their respective modules
from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

def run_etl_pipeline():
    # 🚀 Start the ETL pipeline
    print("🚀 Starting Anime ETL Pipeline...")

    # 📥 Extract data from the API
    data = extract_data()
    print("✅ Data extracted.")

    # 🧼 Transform and clean the data
    transformed = transform_data(data)
    print("✅ Data transformed.")

    # 💾 Load the data into the PostgreSQL database
    load_data(transformed)
    print("✅ Data loaded.")

    # ✅ Done!
    print("🎉 Done!")

# Entry point
if __name__ == "__main__":
    run_etl_pipeline()
