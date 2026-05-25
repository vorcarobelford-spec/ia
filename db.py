import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Criar tabela se não existir
cur.execute("""
CREATE TABLE IF NOT EXISTS memoria (
    id SERIAL PRIMARY KEY,
    texto TEXT
)
""")
conn.commit()


def salvar(texto):
    try:
        cur.execute("INSERT INTO memoria (texto) VALUES (%s)", (texto,))
        conn.commit()
    except Exception as e:
        print("Erro ao salvar memória:", e)


def buscar(query=None):
    try:
        cur.execute("SELECT texto FROM memoria ORDER BY id DESC LIMIT 50")
        rows = [r[0] for r in cur.fetchall()]

        # Busca simples inteligente
        if query:
            relevantes = [r for r in rows if query.lower() in r.lower()]
            if relevantes:
                return "\n".join(relevantes[-5:])

        return "\n".join(rows[-10:])

    except Exception as e:
        print("Erro ao buscar memória:", e)
        return ""
