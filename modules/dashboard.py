# Fonction du dashbord
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