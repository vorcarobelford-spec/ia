from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from memory import salvar, buscar
import os

app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class Msg(BaseModel):
    texto: str

@app.post("/ia")
def ia(msg: Msg):
    try:
        contexto = buscar()

        prompt = f"""
Contexto da conversa:
{contexto}

Usuário: {msg.texto}
IA:
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        resposta = response.text

        # salvar aprendizado
        salvar(f"Usuário: {msg.texto}")
        salvar(f"IA: {resposta}")

        return {"resposta": resposta}

    except Exception as e:
        return {"erro": str(e)}
