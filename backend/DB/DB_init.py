import sqlite3
import os

# Path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/database.db")


def init_db():
    """
    Initializes the database with required tables if they do not exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create device_mappings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_type_mappings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            output_type TEXT UNIQUE,
            device_type TEXT
        )
    """)
    conn.commit()
    conn.close()
