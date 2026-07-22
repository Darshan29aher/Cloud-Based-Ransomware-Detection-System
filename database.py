import sqlite3

DB_NAME = "database/ransomware.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        event_time TEXT,

        event_type TEXT,

        severity TEXT,

        file_name TEXT

    )
    """)

    conn.commit()
    conn.close()


def insert_event(event_time, event_type, severity, file_name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO events(event_time,event_type,severity,file_name)

    VALUES(?,?,?,?)

    """, (event_time, event_type, severity, file_name))

    conn.commit()

    conn.close()


if __name__ == "__main__":
    init_db()