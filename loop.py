import time
import requests
from agent import executar
from memory import adicionar, buscar
from rules import verificar, adicionar as add_rule
from monitor import ler_logs

URL = "https://ia-production-2652.up.railway.app/ia"


def perguntar_ia(contexto):
    try:
        r = requests.post(URL, json={"texto": contexto}, timeout=15)
        return r.json().get("resposta", "")
    except:
        return "AÇÃO: none\nMOTIVO: erro"


while True:
    print("\n🔍 Monitorando...")

    logs = ler_logs()
    memoria = buscar(logs)

    contexto = f"""
Você é um agente inteligente.

Logs recentes:
{logs}

Memória relevante:
{memoria}

Decida ação.

Formato:
AÇÃO: comando_ou_none
MOTIVO: explicação
"""

    resposta = perguntar_ia(contexto)

    print("\n🧠 IA:")
    print(resposta)

    # extrair ação
    if "AÇÃO:" in resposta:
        comando = [l for l in resposta.split("\n") if "AÇÃO:" in l][0]
        comando = comando.replace("AÇÃO:", "").strip()

        # verificar regra primeiro
        regra = verificar(logs)

        if regra:
            print(f"\n⚡ Regra ativada: {regra}")
            comando = regra

        if comando != "none":
            print(f"\n⚡ Executando: {comando}")
            resultado = executar(comando)
            print(resultado)

            adicionar(logs, comando, resultado)

    time.sleep(10)
