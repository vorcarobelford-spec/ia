import json
import os

ARQ = "memoria.json"


def carregar():
    if not os.path.exists(ARQ):
        return []
    with open(ARQ, "r") as f:
        return json.load(f)


def salvar(mem):
    with open(ARQ, "w") as f:
        json.dump(mem, f, indent=2)


def adicionar(situacao, acao, resultado):
    mem = carregar()
    mem.append({
        "situacao": situacao,
        "acao": acao,
        "resultado": resultado
    })
    salvar(mem)


def buscar(situacao):
    mem = carregar()
    relevantes = []

    for m in mem:
        if situacao.lower() in m["situacao"].lower():
            relevantes.append(m)

    return relevantes[-5:]
