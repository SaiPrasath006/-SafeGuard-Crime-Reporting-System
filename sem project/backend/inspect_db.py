import sqlite3
import os

db_path = os.path.join('instance', 'crime_system.db')
if not os.path.exists(db_path):
    # Try alternate path if not in instance
    db_path = 'crime_system.db'

print(f"Checking database at: {os.path.abspath(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(crime_report)")
    columns = cursor.fetchall()
    print("Columns in 'crime_report' table:")
    for col in columns:
        print(f" - {col[1]} ({col[2]})")
    conn.close()
else:
    print("Database file not found.")
