#!/usr/bin/env python3

import os
import pandas as pd
from load import load_data
from model import train_model
from dotenv import load_dotenv
from extract import extract_data
from alert import send_email_alert
from sqlalchemy import create_engine
from transform import transform_data

load_dotenv(override=True)

# Load environment variables
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname = os.getenv('DB_NAME')
port = os.getenv('DB_PORT', '5432')  # default to '5432' as a string

# Connect to DB
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

def run_etl_pipeline():
    """Run the ETL process."""

    print("🚀 Starting ETL pipeline...")

    print("Extracting data...")
    raw = extract_data()
    print("Transforming data...")
    clean = transform_data(raw)
    print("Loading data...")
    load_data(clean)

    print("Loading data from DB for ML training...")
    
    data = pd.read_sql("SELECT * FROM flights", engine)
    
    print("Training model...")
    model = train_model(data)
    
    print("ETL + ML pipeline completed!")

if __name__ == '__main__':
    try:
        run_etl_pipeline()
    except Exception as e:
        error_message = f"🚨 ETL pipeline failed:\n{str(e)}"
        send_email_alert("🚨 Flight ETL Pipeline Failure", error_message)
    
