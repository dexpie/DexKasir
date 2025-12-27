from database.db import Database
import sqlite3

def clean_money_string(value):
    if isinstance(value, str):
        return float(value.replace('Rp', '').replace('.', '').replace(' ', '').strip())
    return float(value)

def migrate():
    print("Starting migration...")
    db = Database()
    db.connect()
    cursor = db.conn.cursor()

    # 1. Update Products Table: Add 'barcode'
    try:
        cursor.execute("ALTER TABLE products ADD COLUMN barcode TEXT UNIQUE")
        print("Added 'barcode' column to products.")
    except sqlite3.OperationalError as e:
        print(f"Skipping products update: {e}")

    # 2. Update Transactions Table: Add 'subtotal', 'discount', 'tax', 'final_total'
    # SQLite doesn't support multiple ADD COLUMN in one statement easily, so we do one by one.
    cols = {
        'subtotal': 'REAL DEFAULT 0', 
        'discount': 'REAL DEFAULT 0', 
        'tax': 'REAL DEFAULT 0', 
        'final_total': 'REAL DEFAULT 0'
    }
    
    for col, dtype in cols.items():
        try:
            cursor.execute(f"ALTER TABLE transactions ADD COLUMN {col} {dtype}")
            print(f"Added '{col}' column to transactions.")
        except sqlite3.OperationalError as e:
            print(f"Skipping transactions update for {col}: {e}")

    # 3. Data Backfill (Optional but good for consistency)
    # We should update final_total = total_amount for existing records
    # and subtotal = total_amount (assuming 0 tax/discount for old ones)
    cursor.execute("SELECT id, total_amount FROM transactions")
    rows = cursor.fetchall()
    for row in rows:
        t_id = row['id']
        total = row['total_amount']
        cursor.execute('''
            UPDATE transactions 
            SET subtotal = ?, final_total = ? 
            WHERE id = ?
        ''', (total, total, t_id))
    
    print("Backfilled existing transaction data.")

    db.conn.commit()
    db.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    migrate()
