import sqlite3

conn = sqlite3.connect("kasir.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(transactions)")
columns = cursor.fetchall()
print("Columns in transactions table:")
for col in columns:
    print(col)
conn.close()
