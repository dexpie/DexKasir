from database.db import Database

class ProductModel:
    def __init__(self):
        self.db = Database()

    def get_all_products(self):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = [dict(row) for row in cursor.fetchall()]
        self.db.close()
        return products

    def get_product_by_barcode(self, barcode):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE barcode = ?", (barcode,))
        product = cursor.fetchone()
        self.db.close()
        if product:
            return dict(product)
        return None

    def add_product(self, name, price, stock, barcode=None):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("INSERT INTO products (name, price, stock, barcode) VALUES (?, ?, ?, ?)", (name, price, stock, barcode))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
        finally:
            self.db.close()

    def update_product(self, product_id, name, price, stock, barcode=None):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("UPDATE products SET name = ?, price = ?, stock = ?, barcode = ? WHERE id = ?", (name, price, stock, barcode, product_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
        finally:
            self.db.close()

    def delete_product(self, product_id):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
        finally:
            self.db.close()
    
    def update_stock(self, product_id, quantity):
        """Reduce stock (quantity is positive to reduce)"""
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
        finally:
            self.db.close()
