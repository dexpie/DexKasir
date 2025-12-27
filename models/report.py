from database.db import Database

class ReportModel:
    def __init__(self):
        self.db = Database()

    def get_daily_sales(self, date_str):
        """Get transactions for a specific date (YYYY-MM-DD)."""
        self.db.connect()
        cursor = self.db.conn.cursor()
        # SQLite date string comparison
        cursor.execute("SELECT * FROM transactions WHERE date(date) = ?", (date_str,))
        transactions = [dict(row) for row in cursor.fetchall()]
        
        total_revenue = sum(t['final_total'] for t in transactions)
        self.db.close()
        return transactions, total_revenue

    def get_monthly_sales(self, month, year):
        """Get transactions for a specific month and year."""
        self.db.connect()
        cursor = self.db.conn.cursor()
        # SQLite strftime('%m', date) returns '01'-'12', %Y returns Year
        cursor.execute("SELECT * FROM transactions WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (f"{month:02d}", str(year)))
        transactions = [dict(row) for row in cursor.fetchall()]
        
        total_revenue = sum(t['final_total'] for t in transactions)
        self.db.close()
        return transactions, total_revenue
