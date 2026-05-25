from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from db import salvar, buscar

app = FastAPI()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# MENOS MODELOS = MAIS ESTÁVEL
modelos = [
    "deepseek/deepseek-v4-flash:free",
     "poolside/laguna-m.1:free",
     "openrouter/owl-alpha",
]


class Msg(BaseModel):
    texto: str


@app.get("/")
def home():
    return {"status": "IA ESTÁVEL ONLINE 🧠🔥"}


@app.post("/ia")
def ia(msg: Msg):
    try:
        ctx = buscar(msg.texto)

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
                    timeout=10  # 🔥 reduzido
                )

                data = response.json()

                if "choices" in data:
                    resposta = data["choices"][0]["message"]["content"]

                    salvar(f"Usuário: {msg.texto}")
                    salvar(f"IA: {resposta}")

                    return {
                        "modelo": modelo,
                        "resposta": resposta
                    }

            except:
                continue

        return {"erro": "Nenhum modelo respondeu"}

    except Exception as e:
        return {"erro": str(e)}
