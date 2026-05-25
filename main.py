from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from db import salvar, buscar

app = FastAPI()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================
# MODELOS (fallback automático)
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
    return {"status": "IA MULTI-MODELO COM MEMÓRIA 🧠🔥"}


@app.post("/ia")
def ia(msg: Msg):
    try:
        # Buscar memória relevante
        ctx = buscar(msg.texto)

        prompt = f"""
Você é uma IA inteligente que aprende com o usuário.

Regras:
- Lembre das preferências do usuário
- Adapte sua forma de falar
- Seja clara e direta
- Evolua com o tempo

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
                    timeout=25
                )

                data = response.json()
                print(f"\nModelo usado: {modelo}\n", data)

                if "choices" in data:
                    resposta = data["choices"][0]["message"]["content"]

                    # Salvar memória permanente
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
