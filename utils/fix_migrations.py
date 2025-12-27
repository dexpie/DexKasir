import sqlite3
import os

DB_NAME = "kasir.db"

def fix_migrations():
    if not os.path.exists(DB_NAME):
        print(f"{DB_NAME} not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [info[1] for info in cursor.fetchall()]
        print(f"Current columns: {columns}")
        
        # Missing columns to check
        new_cols = {
            'subtotal': "REAL DEFAULT 0",
            'discount': "REAL DEFAULT 0",
            'tax': "REAL DEFAULT 0",
            'final_total': "REAL DEFAULT 0",
            'payment_method': "TEXT DEFAULT 'CASH'"
        }
        
        for col, dtype in new_cols.items():
            if col not in columns:
                print(f"Adding missing column: {col}")
                cursor.execute(f"ALTER TABLE transactions ADD COLUMN {col} {dtype}")
                
        # Products table barcode check (Phase 2)
        cursor.execute("PRAGMA table_info(products)")
        p_columns = [info[1] for info in cursor.fetchall()]
        if 'barcode' not in p_columns:
            print("Adding missing column: barcode to products")
            cursor.execute("ALTER TABLE products ADD COLUMN barcode TEXT")

        conn.commit()
        print("Database schema repair completed!")

    except Exception as e:
        print(f"Fix failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_migrations()
