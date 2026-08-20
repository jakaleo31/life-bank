import sqlite3
import os
import contextlib


@contextlib.contextmanager
def get_db_connection():
    """
    Kontekstni manager, ki vrne povezavo do SQLite baze.
    Samodejno zapre povezavo tudi ob napaki.
    Uporaba:
        with get_db_connection() as conn:
            ...
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base_dir, "database")

    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    db_path = os.path.join(db_dir, "manager.db")
    conn = sqlite3.connect(db_path)
    try:
        _inicializiraj_shemo(conn)
        conn.commit()
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _inicializiraj_shemo(conn):
    """Ustvari tabele in vstavi privzete vrednosti, če še ne obstajajo."""
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS transakcije ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'tip TEXT, znesek REAL, datum TEXT, opis TEXT, kategorija TEXT)'
    )
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS dogodki ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'naslov TEXT, datum_zacetek TEXT, datum_konec TEXT, '
        'ura_od TEXT, ura_do TEXT, barva TEXT, opis TEXT)'
    )

    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('hourly_rate', '7.73')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('premium', '0')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('theme_path', 'System')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('savings_goal', '1000')")