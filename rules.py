import json
import os

ARQ = "rules.json"


def carregar():
    if not os.path.exists(ARQ):
        return []
    with open(ARQ, "r") as f:
        return json.load(f)


def salvar(rules):
    with open(ARQ, "w") as f:
        json.dump(rules, f, indent=2)


def adicionar(condicao, acao):
    rules = carregar()
    rules.append({
        "condicao": condicao,
        "acao": acao
    })
    salvar(rules)


def verificar(contexto):
    rules = carregar()

    for r in rules:
        if r["condicao"].lower() in contexto.lower():
            return r["acao"]

    return None
