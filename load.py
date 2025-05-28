import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'dbname': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', 5432)
}

def load_data(data):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                id SERIAL PRIMARY KEY,
                airline VARCHAR(100),
                flight_number VARCHAR(20),
                departure_airport VARCHAR(100),
                arrival_airport VARCHAR(100),
                departure_time TIMESTAMP,
                arrival_time TIMESTAMP,
                status VARCHAR(50)
            )
        """)

        insert_query = """
            INSERT INTO flights (
                airline, flight_number, departure_airport, arrival_airport,
                departure_time, arrival_time, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        for flight in data:
            row = (
                flight.get('airline'),  # already just name string
                flight.get('flight_number'),
                flight.get('departure_airport'),
                flight.get('arrival_airport'),
                flight.get('departure_time'),
                flight.get('arrival_time'),
                flight.get('status')
            )

            # Optional debug:
            #print("Full SQL:", cursor.mogrify(insert_query, row).decode())

            cursor.execute(insert_query, row)

        conn.commit()
        print("✅ Data successfully loaded into PostgreSQL.")
        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Error loading data:", e)
