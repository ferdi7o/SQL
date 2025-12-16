import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",      # senin db adın
    user="postgres",          # kullanıcı adın
    password=""         # PostgreSQL şifren
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM users;")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
