import subprocess

def monitorar_script(arquivo="script.log"):
    try:
        output = subprocess.check_output(
            f"tail -n 20 {arquivo}",
            shell=True,
            text=True
        )
        return output
    except:
        return ""
