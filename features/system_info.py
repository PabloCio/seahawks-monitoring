
import subprocess
import socket
import netifaces

_network_range = None

def get_network_range():
    """
    Retourne la plage réseau sous la forme '192.168.1.138/24'.
    Cette valeur est calculée une seule fois et stockée.
    """
    global _network_range
    if _network_range is None:  # Si on n'a pas encore calculé la valeur
        ip = get_local_ip()
        cidr = get_cidr()
        if ip and cidr is not None:
            _network_range = f"{ip}/{cidr}"  # Stocke la valeur une fois
        else:
            _network_range = "Indisponible"
    
    return _network_range  # Retourne la même valeur pour chaque appel

def update_network_range():
    """
    Réinitialise la plage réseau stockée pour forcer un recalcul.
    """
    global _network_range
    _network_range = None  # Force un recalcul à la prochaine demande

def get_local_ip():
    """
    Retourne l'adresse IP locale de la machine
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
    return None

def get_hostname():
    """
    Retourne le nom d'hôte (hostname) de la machine locale.
    """
    try:
        return socket.gethostname()
    except Exception as e:
        print(f" Erreur lors de la récupération du hostname : {e}")
        return None