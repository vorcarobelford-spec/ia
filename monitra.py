import subprocess

def ler_logs():
    try:
        output = subprocess.check_output(
            "tail -n 20 /var/log/syslog",
            shell=True,
            text=True
        )
        return output
    except:
        return ""
def ler_script_log():
    try:
        return subprocess.check_output(
            "tail -n 20 script.log",
            shell=True,
            text=True
        )
    except:
        return ""
