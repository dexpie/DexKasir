from database.db import Database
from datetime import datetime

class TransactionModel:
    def __init__(self):
        self.db = Database()

    def create_transaction(self, cashier_name, items, subtotal, discount, tax, final_total, payment_method="CASH", member_id=None):
        """
        Create a new transaction and its items.
        """
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            # 1. Insert Transaction Header
            cursor.execute('''
                INSERT INTO transactions (total_amount, subtotal, discount, tax, final_total, cashier_name, payment_method, member_id, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'SUCCESS')
            ''', (final_total, subtotal, discount, tax, final_total, cashier_name, payment_method, member_id))
            transaction_id = cursor.lastrowid

            # 2. Insert Transaction Items
            for item in items:
                cursor.execute('''
                    INSERT INTO transaction_items (transaction_id, product_name, price_at_sale, quantity, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (transaction_id, item['name'], item['price'], item['qty'], item['subtotal']))
                
                # 3. Update Product Stock
                cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (item['qty'], item['product_id']))

            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating transaction: {e}")
            self.db.conn.rollback()
            return False
        finally:
            self.db.close()

    def refund_transaction(self, transaction_id):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            # Check if already refunded
            cursor.execute("SELECT status FROM transactions WHERE id = ?", (transaction_id,))
            status = cursor.fetchone()[0]
            if status == 'REFUNDED':
                return False, "Transaksi sudah di-refund sebelumnya."

            # Restore Stock
            cursor.execute("SELECT product_name, quantity FROM transaction_items WHERE transaction_id = ?", (transaction_id,))
            items = cursor.fetchall()
            
            # This is a bit tricky because we stored product_name, not ID in items table (design flaw in V1/V2). 
            # We try to match by name.
            for name, qty in items:
                cursor.execute("UPDATE products SET stock = stock + ? WHERE name = ?", (qty, name))

            # Update Status
            cursor.execute("UPDATE transactions SET status = 'REFUNDED' WHERE id = ?", (transaction_id,))
            
            self.db.conn.commit()
            return True, "Refund berhasil. Stok dikembalikan."
        except Exception as e:
            self.db.conn.rollback()
            return False, str(e)
        finally:
            self.db.close()

    def get_all_transactions(self):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        transactions = [dict(row) for row in cursor.fetchall()]
        self.db.close()
        return transactions

    def get_transaction_items(self, transaction_id):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM transaction_items WHERE transaction_id = ?", (transaction_id,))
        items = [dict(row) for row in cursor.fetchall()]
        self.db.close()
        return items
