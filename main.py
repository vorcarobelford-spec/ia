from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Msg(BaseModel):
    texto: str

@app.get("/")
def home():
    return {"status": "IA ONLINE 🚀"}

@app.post("/ia")
def ia(msg: Msg):
    return {"resposta": f"Você disse: {msg.texto}"}
