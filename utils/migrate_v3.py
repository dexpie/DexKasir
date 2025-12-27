import sqlite3
import os

DB_NAME = "kasir.db"

def migrate_v3():
    if not os.path.exists(DB_NAME):
        print("Database not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'payment_method' not in columns:
            print("Adding 'payment_method' column to transactions table...")
            cursor.execute("ALTER TABLE transactions ADD COLUMN payment_method TEXT DEFAULT 'CASH'")
            conn.commit()
            print("Migration V3 successful!")
        else:
            print("'payment_method' column already exists.")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_v3()
