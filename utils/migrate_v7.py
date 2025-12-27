import sqlite3
import os

DB_NAME = "kasir.db"

def migrate_v7():
    if not os.path.exists(DB_NAME):
        print(f"{DB_NAME} not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Create Audit Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT
            )
        ''')
        print("Created 'audit_logs' table.")
        
        conn.commit()
        print("Migration V7 successful!")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_v7()
