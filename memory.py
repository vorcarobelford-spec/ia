memoria = []

def salvar(texto):
    memoria.append(texto)

def buscar():
    return "\n".join(memoria[-5:])  # últimas 5 interações
