import json
import os

ARQ = "aprendizado.json"


def carregar():
    if not os.path.exists(ARQ):
        return []
    with open(ARQ, "r") as f:
        return json.load(f)


def salvar(data):
    with open(ARQ, "w") as f:
        json.dump(data, f, indent=2)


def registrar(erro, comando, resultado):
    data = carregar()

    data.append({
        "erro": erro,
        "comando": comando,
        "resultado": resultado
    })

    salvar(data)


def sugerir(erro):
    data = carregar()

    for item in reversed(data):
        if erro.lower() in item["erro"].lower():
            return item["comando"]

    return None
