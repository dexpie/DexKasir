from database.db import Database

class PromoModel:
    def __init__(self):
        self.db = Database()

    def get_promo(self, code):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM promos WHERE code = ? AND active = 1", (code,))
        row = cursor.fetchone()
        self.db.close()
        if row:
            # Row to dict
            return {
                'id': row[0],
                'code': row[1],
                'type': row[2],
                'value': row[3]
            }
        return None

    def create_promo(self, code, discount_type, value):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("INSERT INTO promos (code, discount_type, value) VALUES (?, ?, ?)", (code, discount_type, value))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.db.close()
