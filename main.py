from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================
# MEMÓRIA GLOBAL (única)
# =========================
memoria = []

def salvar(texto):
    memoria.append(texto)

def contexto():
    return "\n".join(memoria[-10:])  # últimas 10 interações


# =========================
# MODELOS (ORDEM DE PRIORIDADE)
# =========================
modelos = [
    "deepseek/deepseek-v4-flash:free",
    "baidu/cobuddy:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "poolside/laguna-xs.2:free",
    "poolside/laguna-m.1:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "nvidia/nemotron-nano-9b-v2:free",
    "meta-llama/llama-3-8b-instruct:free"
]


class Msg(BaseModel):
    texto: str


@app.get("/")
def home():
    return {"status": "IA MULTI-MODELO ONLINE 🧠🔥"}


@app.post("/ia")
def ia(msg: Msg):
    try:
        ctx = contexto()

        prompt = f"""
Você é uma IA inteligente que aprende com o usuário.

Memória:
{ctx}

Usuário: {msg.texto}
IA:
"""

        for modelo in modelos:
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": modelo,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ]
                    },
                    timeout=20
                )

                data = response.json()
                print(f"\nModelo usado: {modelo}\n", data)

                if "choices" in data:
                    resposta = data["choices"][0]["message"]["content"]

                    # salvar memória
                    salvar(f"Usuário: {msg.texto}")
                    salvar(f"IA: {resposta}")

                    return {
                        "modelo": modelo,
                        "resposta": resposta
                    }

            except Exception as e:
                print(f"Erro no modelo {modelo}: {e}")
                continue

        return {"erro": "Nenhum modelo respondeu"}

    except Exception as e:
        return {"erro": str(e)}
