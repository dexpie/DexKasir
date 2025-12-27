import sqlite3
from datetime import datetime
from database.db import Database

class AttendanceModel:
    def __init__(self):
        self.db = Database()

    def clock_in(self, username):
        today = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M:%S")
        
        # Check if already clocked in
        status = self.check_today(username)
        if status and status['clock_in']:
            return False, "Already Clocked In"
            
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("INSERT INTO attendance (username, date, clock_in) VALUES (?, ?, ?)", (username, today, now))
            self.db.conn.commit()
            return True, "Clock In Successful"
        except Exception as e:
            return False, str(e)
        finally:
            self.db.close()

    def clock_out(self, username):
        today = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M:%S")
        
        status = self.check_today(username)
        if not status:
            return False, "Not Clocked In yet"
        if status['clock_out']:
            return False, "Already Clocked Out"
            
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("UPDATE attendance SET clock_out = ? WHERE id = ?", (now, status['id']))
            self.db.conn.commit()
            return True, "Clock Out Successful"
        except Exception as e:
            return False, str(e)
        finally:
            self.db.close()

    def check_today(self, username):
        today = datetime.now().strftime("%Y-%m-%d")
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM attendance WHERE username = ? AND date = ?", (username, today))
        row = cursor.fetchone()
        self.db.close()
        
        if row:
            return {'id': row[0], 'username': row[1], 'date': row[2], 'clock_in': row[3], 'clock_out': row[4]}
        return None
        
    def get_history(self, limit=30):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM attendance ORDER BY date DESC, clock_in DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        self.db.close()
        return rows
