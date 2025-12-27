import sqlite3
import os

DB_NAME = "kasir.db"

def migrate_v5():
    if not os.path.exists(DB_NAME):
        print(f"{DB_NAME} not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # 1. Update Products Table: Add cost_price
        cursor.execute("PRAGMA table_info(products)")
        cols = [info[1] for info in cursor.fetchall()]
        if 'cost_price' not in cols:
            cursor.execute("ALTER TABLE products ADD COLUMN cost_price REAL DEFAULT 0")
            print("Added 'cost_price' to products.")

        # 2. Update Transaction Items Table: Add cost_at_sale
        cursor.execute("PRAGMA table_info(transaction_items)")
        cols = [info[1] for info in cursor.fetchall()]
        if 'cost_at_sale' not in cols:
            cursor.execute("ALTER TABLE transaction_items ADD COLUMN cost_at_sale REAL DEFAULT 0")
            print("Added 'cost_at_sale' to transaction_items.")

        # 3. Create Shifts Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cashier_name TEXT NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                start_cash REAL DEFAULT 0,
                end_cash REAL DEFAULT 0,
                actual_cash REAL,
                status TEXT DEFAULT 'OPEN'
            )
        ''')
        print("Created 'shifts' table.")

        conn.commit()
        print("Migration V5 successful!")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_v5()
