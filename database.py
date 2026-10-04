import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set.")

    return psycopg2.connect(DATABASE_URL)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price DOUBLE PRECISION NOT NULL,
            stock_quantity INTEGER NOT NULL,
            reorder_level INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_amount DOUBLE PRECISION NOT NULL,
            sale_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()

def add_supplier_relationship():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        ALTER TABLE products
        ADD COLUMN IF NOT EXISTS supplier_id INTEGER
        REFERENCES suppliers(id)
    """)

    connection.commit()

    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_tables()
    add_supplier_relationship()
    print("Database tables created successfully!")