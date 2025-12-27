import sqlite3
from datetime import datetime
from database.db import Database

class ExpenseModel:
    def __init__(self):
        self.db = Database()

    def add_expense(self, category, amount, description, user):
        today = datetime.now().strftime("%Y-%m-%d")
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("INSERT INTO expenses (date, category, amount, description, user) VALUES (?, ?, ?, ?, ?)", 
                           (today, category, amount, description, user))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.db.close()

    def get_expenses(self, start_date=None, end_date=None):
        self.db.connect()
        cursor = self.db.conn.cursor()
        if start_date and end_date:
            cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC", (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM expenses ORDER BY date DESC LIMIT 100")
        rows = cursor.fetchall()
        self.db.close()
        
        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'date': row[1],
                'category': row[2],
                'amount': row[3],
                'description': row[4],
                'user': row[5]
            })
        return result

    def get_total_expenses(self, start_date, end_date):
        expenses = self.get_expenses(start_date, end_date)
        return sum(e['amount'] for e in expenses)
