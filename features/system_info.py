
#Fonction de latance
import subprocess
import socket
from scan import scan_network

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
        print(f" Erreur lors de la récupération du hostname : {e}")
        return None

# 🔥 Exemple d'utilisation :
print(get_hostname())  # Affiche le hostname de la machine





def get_local_ip():
    """
    Retourne l'adresse IP locale de la machine.
    """
    try:
        # Crée un socket temporaire pour obtenir l'IP sans nécessiter de connexion réelle
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Se connecte à Google DNS (mais sans envoyer de données)
        ip_locale = s.getsockname()[0]  # Récupère l'adresse IP locale
        s.close()
        return ip_locale
    except Exception as e:
        print(f" Erreur lors de la récupération de l'IP locale : {e}")
        return None

# 🔥 Exemple d'utilisation :
# print(get_local_ip())  # Affiche l'adresse IP locale

def get_connected_devices_count(network_range):
    """
    Scanne le réseau et retourne le nombre d'appareils connectés (sans scanner les ports).
    
    :param network_range: La plage d'IP à scanner (ex: "192.168.1.0/24")
    :return: Nombre d'appareils actifs détectés
    """
    devices = scan_network(network_range)  # Appelle la fonction scan_network
    return len(devices)  # Retourne le nombre total de machines trouvées

# 🔥 Exemple d'utilisation :
network_range = "192.168.1.0/24"  # Modifie selon ton réseau
print(f"Appareils connectés : {get_connected_devices_count(network_range)}")

