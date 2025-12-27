import sqlite3
import os

DB_NAME = "kasir.db"

def migrate_v4():
    if not os.path.exists(DB_NAME):
        print(f"{DB_NAME} not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # 1. Create Members Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                points INTEGER DEFAULT 0
            )
        ''')
        print("Created 'members' table.")

        # 2. Update Transactions Table
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'member_id' not in columns:
            cursor.execute("ALTER TABLE transactions ADD COLUMN member_id INTEGER")
            print("Added 'member_id' to transactions.")
            
        if 'status' not in columns:
            cursor.execute("ALTER TABLE transactions ADD COLUMN status TEXT DEFAULT 'SUCCESS'")
            print("Added 'status' to transactions.")

        conn.commit()
        print("Migration V4 successful!")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_v4()
