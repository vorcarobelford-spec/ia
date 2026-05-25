from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

API_KEY = os.getenv("OPENROUTER_API_KEY")

class Msg(BaseModel):
    texto: str

@app.post("/ia")
def ia(msg: Msg):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": msg.texto}
                ]
            }
        )

        data = response.json()

        # DEBUG (importante)
        print(data)

        if "choices" in data:
            return {
                "resposta": data["choices"][0]["message"]["content"]
            }
        else:
            return {"erro_api": data}

    except Exception as e:
        return {"erro": str(e)}
