import time
from agent import executar
import requests

URL = "https://ia-production-2652.up.railway.app/ia"

def perguntar_ia(contexto):
    r = requests.post(URL, json={"texto": contexto})
    return r.json().get("resposta", "")


while True:
    print("\n🔍 Observando sistema...")

    # exemplo: ver processos
    estado = executar("ps aux | head -n 5")

    prompt = f"""
Você é um agente inteligente.

Estado atual:
{estado}

Decida:
- o que está acontecendo
- se precisa agir
- qual comando executar (se necessário)

Responda no formato:
AÇÃO: comando_ou_none
MOTIVO: explicação
"""

    resposta = perguntar_ia(prompt)

    print("\n🧠 IA decidiu:")
    print(resposta)

    if "AÇÃO:" in resposta:
        linha = [l for l in resposta.split("\n") if "AÇÃO:" in l]

        if linha:
            comando = linha[0].replace("AÇÃO:", "").strip()

            if comando != "none":
                print(f"\n⚡ Executando: {comando}")
                output = executar(comando)
                print(output)

    time.sleep(10)
