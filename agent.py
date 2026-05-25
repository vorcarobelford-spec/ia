import subprocess

def executar(comando):
    try:
        resultado = subprocess.check_output(
            comando,
            shell=True,
            stderr=subprocess.STDOUT,
            text=True
        )
        return resultado
    except subprocess.CalledProcessError as e:
        return e.output
