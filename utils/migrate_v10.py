import sqlite3
import os

DB_NAME = "kasir.db"

def migrate_v10():
    if not os.path.exists(DB_NAME):
        print(f"{DB_NAME} not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Create Expenses Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                user TEXT
            )
        ''')
        print("Created 'expenses' table.")
        
        conn.commit()
        print("Migration V10 successful!")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_v10()
