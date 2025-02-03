import socket

VERSION = 1.0

def get_info_machine():
        # Retourne les informations de la machine locale : hostname, IP locale et version de l'application.
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            version = VERSION
            return {"hostname": hostname, "local_ip": local_ip, "version": version}
        except socket.error as e:
            return {"error": f"Erreur : {e}"}
        
# Récupérer les infos de la machine
info = get_info_machine()
print(info)

import netifaces
import ipaddress

def get_network_range(local_ip):
    """
    Détermine la plage réseau (CIDR) exacte de la machine locale en fonction de son adresse IP et de son masque.
    Fonctionne pour tous les masques : /32, /24, /16, etc.
    """
    try:
        # Trouver l'interface associée à cette IP
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr.get('addr')
                    netmask = addr.get('netmask')

                    if ip == local_ip and netmask:
                        # Calculer la plage réseau exacte avec le masque
                        network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                        return str(network)

        return "Impossible de déterminer la plage réseau."

    except Exception as e:
        return f"Erreur : {e}"

# Vérifier si l'IP locale a bien été récupérée avant d'appeler get_network_range
if "local_ip" in info:
    network_range = get_network_range(info["local_ip"])
    print(f"Résultat : {network_range}")
else:
    print("Impossible de récupérer l'IP locale.")