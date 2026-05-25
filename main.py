from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os

app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class Msg(BaseModel):
    texto: str

@app.get("/")
def home():
    return {"status": "IA ONLINE 🧠🔥"}

@app.post("/ia")
def ia(msg: Msg):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=msg.texto
        )

        return {"resposta": response.text}
    
    except Exception as e:
        return {"erro": str(e)}
        
