import socket
import json
import os
import nmap
import netifaces
import ipaddress

def get_info_machine(): # Retourne les informations de la machine locale : hostname, IP locale et version de l'application. 
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        version = 1.3
        return {"hostname": hostname, "local_ip": local_ip, "version": version}
    except socket.error as e:
        return {"error": f"Erreur : {e}"}

# Récupérer les infos de la machine
info = get_info_machine()
print(info)

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

def scan_network(network_range):
    """
    Scanne le réseau donné (exemple : "192.168.1.0/24") et affiche :
      - le nombre de machines actives détectées
      - pour chaque machine, son hostname (si disponible) et la liste de ses ports ouverts (1 à 1024)
    """
    scanner = nmap.PortScanner()
    
    print(f"Scanning network: {network_range}")

    try:
        # Ajout de timeout et optimisation du scan
        scanner.scan(hosts=network_range, arguments='-p 1-40 -T4 --min-hostgroup 64', timeout=300)
    except Exception as e:
        print(f"Erreur lors du scan : {e}")
        return

    machines = {}
    
    for host in scanner.all_hosts():
        if scanner[host].state() == 'up':
            open_ports = []
            for proto in scanner[host].all_protocols():
                for port in scanner[host][proto]:
                    if scanner[host][proto][port]['state'] == 'open':
                        open_ports.append(port)
            hostnames = scanner[host].get('hostnames', [])
            hostname = hostnames[0]['name'] if hostnames and hostnames[0].get('name') else "N/A"
            machines[host] = {"hostname": hostname, "open_ports": open_ports}
    
    print("Nombre de machines détectées :", len(machines))
    for host, data in machines.items():
        print("Machine :", host)
        print("Hostname :", data["hostname"])
        print("Ports ouverts :", data["open_ports"])
        print("-" * 40)

    # Enregistrement en local après le scan
    scan_results = {
        "network": network_range,
        "machines": machines
    }
    save_scan_results_local(scan_results)

def save_scan_results_local(results, filename="scan_results.json"):
    """
    Sauvegarde les résultats du scan dans un fichier JSON.
    """
    try:
        # Vérifie si le fichier existe déjà
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        # Ajoute les nouveaux résultats au fichier existant
        existing_data.append(results)

        # Sauvegarde dans le fichier
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4)

        print(f"Résultats du scan enregistrés dans {filename}")

    except Exception as e:
        print(f"Erreur lors de l'enregistrement des résultats : {e}")

if network_range and "Impossible" not in network_range:
    scan_network(network_range)
else:
    print("Le scan réseau n'a pas été lancé car la plage réseau est invalide.")

