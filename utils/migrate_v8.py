import sqlite3
import os

DB_NAME = "kasir.db"

def migrate_v8():
    if not os.path.exists(DB_NAME):
        print(f"{DB_NAME} not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Add 'debt' column to members
        try:
            cursor.execute("ALTER TABLE members ADD COLUMN debt REAL DEFAULT 0")
            print("Added 'debt' column to members table.")
        except sqlite3.OperationalError:
            print("'debt' column already exists in members.")

        conn.commit()
        print("Migration V8 successful!")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_v8()
