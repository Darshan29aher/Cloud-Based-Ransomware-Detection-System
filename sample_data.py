import sqlite3
from datetime import datetime

conn = sqlite3.connect("database/ransomware.db")
cursor = conn.cursor()

sample_events = [
    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Monitoring Started", "Info", "-"),
    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "File Created", "Low", "document1.txt"),
    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "File Modified", "Medium", "report.docx")
]

cursor.executemany(
    "INSERT INTO events(event_time, event_type, severity, file_name) VALUES (?, ?, ?, ?)",
    sample_events
)

conn.commit()
conn.close()

print("Sample data inserted.")