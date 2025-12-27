import sqlite3
import hashlib

class Database:
    def __init__(self, db_file="kasir.db"):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row # Access columns by name
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()

    def init_db(self):
        """Initialize database tables and seed data."""
        self.connect()
        cursor = self.conn.cursor()

        # Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        # Products Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        ''')

        # Transactions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_amount REAL NOT NULL,
                subtotal REAL DEFAULT 0,
                discount REAL DEFAULT 0,
                tax REAL DEFAULT 0,
                final_total REAL DEFAULT 0,
                cashier_name TEXT NOT NULL,
                payment_method TEXT DEFAULT 'CASH'
            )
        ''')

        # Transaction Items Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaction_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                price_at_sale REAL NOT NULL,
                quantity INTEGER NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (transaction_id) REFERENCES transactions (id)
            )
        ''')

        # Seed Admin User if not exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            # Password 'admin123' hashed
            hashed_pw = hashlib.sha256('admin123'.encode()).hexdigest()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           ('admin', hashed_pw, 'admin'))
            print("Seeded admin user.")

        # Seed Cashier User if not exists
        cursor.execute("SELECT * FROM users WHERE username = 'kasir'")
        if not cursor.fetchone():
             # Password 'kasir123' hashed
            hashed_pw = hashlib.sha256('kasir123'.encode()).hexdigest()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           ('kasir', hashed_pw, 'kasir'))
            print("Seeded cashier user.")
        
        # Seed Initial Products if empty
        cursor.execute("SELECT count(*) FROM products")
        if cursor.fetchone()[0] == 0:
            products = [
                ('Kopi Susu', 15000, 100),
                ('Teh Manis', 5000, 200),
                ('Roti Bakar', 12000, 50),
                ('Mie Goreng', 10000, 80)
            ]
            cursor.executemany("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", products)
            print("Seeded initial products.")

        self.conn.commit()
        self.close()

if __name__ == "__main__":
    db = Database()
    db.init_db()
