from database.db import Database

class MemberModel:
    def __init__(self):
        self.db = Database()

    def add_member(self, name, phone):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("INSERT INTO members (name, phone) VALUES (?, ?)", (name, phone))
            self.db.conn.commit()
            return True, "Member added"
        except Exception as e:
            return False, str(e)
        finally:
            self.db.close()

    def get_member_by_phone(self, phone):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM members WHERE phone = ?", (phone,))
        row = cursor.fetchone()
        self.db.close()
        if row:
            return {'id': row[0], 'name': row[1], 'phone': row[2], 'points': row[3]}
        return None

    def add_points(self, member_id, points):
        self.db.connect()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("UPDATE members SET points = points + ? WHERE id = ?", (points, member_id))
            self.db.conn.commit()
            return True
        except Exception:
            return False
        finally:
            self.db.close()
