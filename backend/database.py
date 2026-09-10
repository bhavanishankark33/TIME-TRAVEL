import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT PRIMARY KEY,
            customer_name TEXT,
            destination TEXT,
            travel_year INTEGER,
            status TEXT,
            price INTEGER
        )
    """)

    bookings = [
    ("2048", "Honey", "Paris", 1889, "confirmed", 45000),
    ("5555", "Bobby", "London", 1920, "timeline error", 38000),
    ("3012", "Jimmy", "Tokyo", 2120, "confirmed", 52000),
    ("7821", "Sunny", "New York", 2026, "confirmed", 30000),
    ("9910", "Mahathi", "New York", 3026, "confirmed", 75000)
]

    cursor.executemany("""
    INSERT INTO bookings
    (booking_id, customer_name, destination, travel_year, status, price)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (booking_id) DO NOTHING
""", bookings)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")