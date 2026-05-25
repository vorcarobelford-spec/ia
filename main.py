from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from db import salvar, buscar
from datetime import datetime

app = FastAPI()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================
# MODELOS (mantidos)
# =========================
modelos = [
    "deepseek/deepseek-v4-flash:free",
    "poolside/laguna-m.1:free",
    "openrouter/owl-alpha",
]


class Msg(BaseModel):
    texto: str


@app.get("/")
def home():
    return {
        "status": "IA ESTÁVEL ONLINE 🧠🔥",
        "modo": "multi-modelo",
        "hora": datetime.now().strftime("%H:%M:%S")
    }


@app.post("/ia")
def ia(msg: Msg):
    try:
        ctx = buscar(msg.texto)

        prompt = f"""
Você é uma IA inteligente.

Responda:
- direto
- organizado
- com parágrafos curtos
- sem enrolação

Memória relevante:
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
                    timeout=10
                )

                data = response.json()

                if "choices" in data:
                    resposta = data["choices"][0]["message"]["content"].strip()

                    # salvar memória
                    salvar(f"Usuário: {msg.texto}")
                    salvar(f"IA: {resposta}")

                    return {
                        "ok": True,
                        "modelo": modelo,
                        "resposta": resposta,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }

            except Exception as e:
                print(f"Erro no modelo {modelo}: {e}")
                continue

        return {
            "ok": False,
            "erro": "Nenhum modelo respondeu"
        }

    except Exception as e:
        return {
            "ok": False,
            "erro": str(e)
        }
