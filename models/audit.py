import sqlite3
from datetime import datetime
from database.db import Database

class AuditModel:
    def __init__(self):
        self.db = Database()

    def log_action(self, user, action, details=""):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("INSERT INTO audit_logs (user, action, details) VALUES (?, ?, ?)", (user, action, details))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Log Error: {e}")
            return False
        finally:
            self.db.close()

    def get_logs(self, limit=100):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        self.db.close()
        
        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'timestamp': row[1],
                'user': row[2],
                'action': row[3],
                'details': row[4]
            })
        return result
