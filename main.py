from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

class Msg(BaseModel):
    texto: str

@app.get("/")
def home():
    return {"status": "IA ONLINE 🧠🔥"}

@app.post("/ia")
def ia(msg: Msg):
    try:
        response = model.generate_content(msg.texto)
        return {"resposta": response.text}
    except Exception as e:
        return {"erro": str(e)}
