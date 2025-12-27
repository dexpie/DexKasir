import sqlite3
import os

DB_NAME = "kasir.db"

def migrate_v9():
    if not os.path.exists(DB_NAME):
        print(f"{DB_NAME} not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Create Attendance Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                date TEXT NOT NULL,
                clock_in TEXT,
                clock_out TEXT
            )
        ''')
        print("Created 'attendance' table.")
        
        # Add 'daily_target' to settings if not exists (handled by key-value store usually)
        # But settings is key-value in db? NO, settings is a table with single row usually or k-v?
        # Check SettingsModel. It uses a 'settings' table? 
        # Actually SettingsModel uses json file or single row? 
        # Wait, let's check SettingsModel code. 
        # Ah, 'settings' table with 'key' and 'value'. So no schema change needed for target.

        conn.commit()
        print("Migration V9 successful!")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_v9()
