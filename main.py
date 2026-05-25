from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("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"))

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
