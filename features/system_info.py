
#Fonction de latance
import subprocess
import socket
#pour windows dans result la lettre doit etre n et dans linux elle doit etre c
def get_wan_latency():
    try:
        result = subprocess.run(["ping", "-n", "1", "8.8.8.8"], capture_output=True, text=True)
        #print(result.stdout)  # Affiche la sortie du ping
        for line in result.stdout.split("\n"):
            if "temps" in line or "time=" in line:
                return float(line.split("time=" if "time=" in line else "temps=")[1].split(" ")[0])
    except Exception as e:
        print(f"Erreur : {e}")
        return None

latency = get_wan_latency()
print(f"Latence vers Google : {latency} ms" if latency else "Impossible de mesurer la latence.")



def get_hostname():
    """
    Retourne le nom d'hôte (hostname) de la machine locale.
    """
    try:
        return socket.gethostname()
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du hostname : {e}")
        return None

# 🔥 Exemple d'utilisation :
print(get_hostname())  # Affiche le hostname de la machine
