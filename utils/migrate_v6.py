import sqlite3
import os

DB_NAME = "kasir.db"

def migrate_v6():
    if not os.path.exists(DB_NAME):
        print(f"{DB_NAME} not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Create Promos Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                discount_type TEXT NOT NULL, -- 'PERCENT' or 'FIXED'
                value REAL NOT NULL,
                active INTEGER DEFAULT 1
            )
        ''')
        print("Created 'promos' table.")

        # Seed initial promo
        try:
            cursor.execute("INSERT INTO promos (code, discount_type, value) VALUES ('WELCOME', 'PERCENT', 10)")
            print("Seeded promo 'WELCOME' (10%).")
        except sqlite3.IntegrityError:
            pass # Already exists

        conn.commit()
        print("Migration V6 successful!")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_v6()
