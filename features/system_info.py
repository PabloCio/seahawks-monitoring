
#Fonction de latance
import subprocess
import socket
import netifaces
from features.scan import scan_network

#pour windows dans result la lettre doit etre n et dans linux elle doit etre c
def get_wan_latency():
    try:
        result = subprocess.run(["ping", "-c", "1", "8.8.8.8"], capture_output=True, text=True) # option -c pour Debian et -n pour Windows
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

#  Exemple d'utilisation :
#print(get_hostname())  # Affiche le hostname de la machine





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
    

# Exemple d'utilisation :
# print(get_local_ip())  # Affiche l'adresse IP locale

def get_connected_devices_count(network_range):
    """
    Scanne le réseau et retourne le nombre d'appareils connectés (sans scanner les ports).
    
    :param network_range: La plage d'IP à scanner (ex: "192.168.1.0/24")
    :return: Nombre d'appareils actifs détectés
    """
    devices = scan_network(network_range)  # Appelle la fonction scan_network
    return len(devices)  # Retourne le nombre total de machines trouvées

#  Exemple d'utilisation :
#network_range = "192.168.1.0/24"  # Modifie selon ton réseau
#print(f"Appareils connectés : {get_connected_devices_count(network_range)}")

def get_netmask(ip_locale):
    """ Récupère le masque réseau de l'interface correspondant à l'IP locale. """
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                if addr['addr'] == ip_locale:
                    return addr['netmask']
    return None  # Si aucune correspondance trouvée

def mask_to_cidr(netmask):
    """ Convertit un masque de sous-réseau (ex. 255.255.255.0) en notation CIDR. """
    return sum(bin(int(x)).count('1') for x in netmask.split('.'))

def get_cidr():
    """ Retourne uniquement le CIDR du réseau actuel (ex. 24 pour /24). """
    try:
        ip_locale = get_local_ip()
        netmask = get_netmask(ip_locale)
        return mask_to_cidr(netmask)

    except Exception as e:
        return print(f"Erreur lors de la récupération du CIDR : {e}")

def get_plage():
    # Retourne l'adresse IP locale avec le CIDR sous forme '192.168.1.50/24'. """
    ip = get_local_ip()
    cidr = get_cidr()

    if ip and cidr is not None:
        return f"{ip}/{cidr}"
    else:
        return None