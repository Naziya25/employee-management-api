
import sqlite3
import os

# Persistent database location
DB_PATH = "/app/data/employees.db"

# Connect to the database
def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# Create employee table
def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
