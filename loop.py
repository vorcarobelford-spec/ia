import time
import requests
from agent import executar
from watcher import monitorar_script
from learning import registrar, sugerir

URL = "https://ia-production-2652.up.railway.app/ia"


def perguntar_ia(contexto):
    try:
        r = requests.post(URL, json={"texto": contexto}, timeout=15)
        return r.json().get("resposta", "")
    except:
        return "AÇÃO: none\nMOTIVO: erro"


while True:
    print("\n🔍 Monitorando script...")

    logs = monitorar_script("script.log")

    # 🧠 tentativa de auto-aprendizado
    sugestao = sugerir(logs)

    if sugestao:
        print(f"\n🧠 Aprendizado encontrado → {sugestao}")
        comando = sugestao
    else:
        prompt = f"""
Você é um agente autônomo.

Analise o log:

{logs}

Se houver erro:
- descubra o problema
- proponha solução

Formato:
AÇÃO: comando_ou_none
MOTIVO: explicação
"""

        resposta = perguntar_ia(prompt)

        print("\n🧠 IA:")
        print(resposta)

        if "AÇÃO:" in resposta:
            comando = [l for l in resposta.split("\n") if "AÇÃO:" in l][0]
            comando = comando.replace("AÇÃO:", "").strip()
        else:
            comando = "none"

    # ⚡ execução
    if comando != "none":
        print(f"\n⚡ Executando: {comando}")
        resultado = executar(comando)
        print(resultado)

        # 💾 aprendizado automático
        registrar(logs, comando, resultado)

    time.sleep(10)
