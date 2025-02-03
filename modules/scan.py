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
    # Permet d'identifier l'interface réseau et son net mask pour le scan
    try:
        # Trouver l'interface associée à IP
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface) # Fontion retournant l'adresse, le netmask et la mac
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]: #netifaces.AF_INET contient l'adresse et le mask
                    ip = addr.get('addr')
                    netmask = addr.get('netmask')

                    if ip == local_ip and netmask: # On compare que l'adresse et le mask retourné correspond bien à l'adresse de la fonction get_info_machine et le mask de AF_INET
                        network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False) # convertie l'adresse et le masque en plage réseau
                        return str(network)

        return "Impossible de déterminer la plage réseau."

    except Exception as e:
        return f"Erreur : {e}"

import nmap

# Fonction scan pour determiner les machines sur le réseau
def scan_network():
    
    # Récupération des informations de la machine locale (IP)
    machine_info = get_info_machine()
    local_ip = machine_info["local_ip"]

    # Déterminer la plage réseau
    network_range = get_network_range(local_ip)
    if not network_range:
        print("Erreur : Impossible de récupérer la plage réseau.")
        return []

    print(f"Scan en cours sur le réseau : {network_range}")

    # Initialisation du scanner nmap
    nm = nmap.PortScanner()

    try:
        # Scan sur les ports 1-65535 en TCP (peut être ajusté selon besoin)
        nm.scan(hosts=network_range, arguments="-p 1-24 -T4 --open")

        machines = []

        # Parcourir les résultats du scan
        for host in nm.all_hosts():
            hostname = nm[host].hostname()
            ports = []

            # Récupérer les ports ouverts
            if 'tcp' in nm[host]:
                for port in nm[host]['tcp']:
                    ports.append({"port": port,"service": nm[host]['tcp'][port]['name']})

            machines.append({"ip": host,"hostname": hostname if hostname else "Inconnu","ports": ports})

        return machines

    except Exception as e:
        print(f"Erreur durant le scan : {e}")
        return []

# Exécuter le scan
if __name__ == "__main__":
    scan_results = scan_network()
    if scan_results:
        print(" Résultats du scan réseau :")
        for device in scan_results:
            print(f" {device['hostname']} - {device['ip']} - Ports ouverts : {', '.join([str(p['port']) for p in device['ports']])}")
    else:
        print("Aucun appareil détecté sur le réseau.")