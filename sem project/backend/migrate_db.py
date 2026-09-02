import sqlite3
import os

db_path = os.path.join('instance', 'crime_system.db')
if not os.path.exists(db_path):
    db_path = 'crime_system.db'

print(f"Migrating database at: {os.path.abspath(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add phone_number if missing
    try:
        cursor.execute("ALTER TABLE crime_report ADD COLUMN phone_number VARCHAR(20)")
        print("Added phone_number column.")
    except sqlite3.OperationalError as e:
        print(f"phone_number column status: {e}")

    # Add aadhar if missing
    try:
        cursor.execute("ALTER TABLE crime_report ADD COLUMN aadhar VARCHAR(20)")
        print("Added aadhar column.")
    except sqlite3.OperationalError as e:
        print(f"aadhar column status: {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")
else:
    print("Database file not found. Initial tables will be created by the app.")
