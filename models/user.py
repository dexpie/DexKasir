from database.db import Database
from utils.helpers import hash_password
import sqlite3

class UserModel:
    def __init__(self):
        self.db = Database()

    def login(self, username, password):
        """authenticate user"""
        self.db.connect()
        cursor = self.db.conn.cursor()
        hashed_pw = hash_password(password)
        
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
        user = cursor.fetchone()
        self.db.close()
        
        if user:
            return dict(user)
        return None

    def get_all_users(self):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        # Initialize an empty list to store user dictionaries
        users = []
        for row in cursor.fetchall():
             # Access by index since Row factory might not be set or behaviour is standard
             users.append({'id': row[0], 'username': row[1], 'role': row[3]})
        self.db.close()
        return users

    def add_user(self, username, password, role):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            hashed = hash_password(password)
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
            self.db.conn.commit()
            return True, "User added"
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            return False, str(e)
        finally:
            self.db.close()

    def delete_user(self, user_id):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.db.conn.commit()
            return True
        except Exception:
            return False
        finally:
            self.db.close()
