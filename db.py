import psycopg2
import os

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# criar tabela
cur.execute("""
CREATE TABLE IF NOT EXISTS memoria (
    id SERIAL PRIMARY KEY,
    texto TEXT
)
""")
conn.commit()


def salvar(texto):
    cur.execute("INSERT INTO memoria (texto) VALUES (%s)", (texto,))
    conn.commit()


def buscar():
    cur.execute("SELECT texto FROM memoria ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    return "\n".join([r[0] for r in rows])
