from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("⚠️ API KEY NÃO ENCONTRADA")

client = OpenAI(api_key=api_key)

class Msg(BaseModel):
    texto: str

@app.get("/")
def home():
    return {"status": "IA ONLINE 🧠🔥"}

@app.post("/ia")
def ia(msg: Msg):
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é uma IA inteligente, útil e direta."},
            {"role": "user", "content": msg.texto}
        ]
    )

    return {"resposta": resposta.choices[0].message.content}

    return {"resposta": resposta.choices[0].message.content}
