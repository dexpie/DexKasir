from database.db import Database
from datetime import datetime

class ShiftModel:
    def __init__(self):
        self.db = Database()

    def start_shift(self, cashier_name, start_cash):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            # Close any existing open shift for safety
            cursor.execute("UPDATE shifts SET status='CLOSED', end_time=CURRENT_TIMESTAMP WHERE status='OPEN'")
            
            cursor.execute('''
                INSERT INTO shifts (cashier_name, start_cash, status)
                VALUES (?, ?, 'OPEN')
            ''', (cashier_name, start_cash))
            self.db.conn.commit()
            return True, "Shift opened."
        except Exception as e:
            return False, str(e)
        finally:
            self.db.close()

    def get_current_shift(self):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM shifts WHERE status = 'OPEN' ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        self.db.close()
        if row:
            return dict(row)
        return None

    def close_shift(self, shift_id, end_cash):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute('''
                UPDATE shifts 
                SET end_cash = ?, status = 'CLOSED', end_time = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (end_cash, shift_id))
            self.db.conn.commit()
            return True, "Shift closed."
        except Exception as e:
            return False, str(e)
        finally:
            self.db.close()
