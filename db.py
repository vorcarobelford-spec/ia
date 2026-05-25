import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def salvar(texto):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO memoria (texto) VALUES (%s)",
            (texto,)
        )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("Erro ao salvar:", e)


def buscar(query=None):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT texto FROM memoria ORDER BY id DESC LIMIT 30")
        rows = [r[0] for r in cur.fetchall()]

        cur.close()
        conn.close()

        if query:
            relevantes = [r for r in rows if query.lower() in r.lower()]
            if relevantes:
                return "\n".join(relevantes[-5:])

        return "\n".join(rows[-10:])

    except Exception as e:
        print("Erro ao buscar:", e)
        return ""
