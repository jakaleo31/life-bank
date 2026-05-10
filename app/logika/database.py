import sqlite3
import os


def get_db_connection():
    # Najdemo pot do mape projekta
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base_dir, "database")

    # Ustvarimo mapo database, če je slučajno ni
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    db_path = os.path.join(db_dir, "manager.db")
    return sqlite3.connect(db_path)
