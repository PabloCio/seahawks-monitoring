import socket
import psutil
import subprocess
import nmap
import json
import os


Class Backend 
VERSION = "1.3"

@staticmethod
def get_info_machine():
    """
    Retourne les informations de la machine locale : hostname, IP locale et version de l'application.
    """
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        version = NetworkScanner.VERSION
        return {"hostname": hostname, "local_ip": local_ip, "version": version}
    except socket.error as e:
        return {"error": f"Erreur : {e}"}

@staticmethod
def get_all_local_ips():
    """
    Retourne toutes les IP locales et leurs interfaces.
    """
    ip_list = []
    try:
        interfaces = psutil.net_if_addrs()
        for iface_name, addresses in interfaces.items():
            for address in addresses:
                if address.family == socket.AF_INET:
                    ip_list.append({"ip": address.address, "interface": iface_name})
        return ip_list
    except Exception as e:
        return [{"error": f"Erreur : {str(e)}"}]

@staticmethod
def test_google_latency():
    """
    Teste la latence du serveur Google (8.8.8.8) et retourne le temps moyen en millisecondes.
    """
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "8.8.8.8"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors="replace"
        )
        if result.returncode == 0 and result.stdout:
            for line in result.stdout.splitlines():
                if "temps" in line or "time" in line:
                    latency_part = line.split("temps=" if "temps" in line else "time=")[1]
                    latency = latency_part.split("ms")[0].strip()
                    return int(latency)
        return None
    except Exception as e:
        return {"error": f"Erreur lors du test de latence : {e}"}

@staticmethod
def run_nmap_scan_on_all_interfaces():
    """
    Effectue un scan réseau sur toutes les interfaces réseau.
    """
    scanner = nmap.PortScanner()
    ip_list = NetworkScanner.get_all_local_ips()
    scan_results = []

    try:
        for ip_info in ip_list:
            ip = ip_info["ip"]
            interface = ip_info["interface"]
            subnet = f"{ip}/24"  # Sous-réseau à scanner
            print(f"Lancement du scan sur le sous-réseau {subnet} (interface: {interface})...")
            scanner.scan(hosts=subnet, arguments="-F")  # Scan rapide (-F) du sous-réseau
            for host in scanner.all_hosts():
                hostname = scanner[host].hostname() or "Nom de machine inconnu"
                host_info = {"host": host, "hostname": hostname, "state": scanner[host].state(), "ports": []}
                if 'tcp' in scanner[host]:
                    for port in sorted(scanner[host]['tcp']):
                        if scanner[host]['tcp'][port]['state'] == 'open':
                            service = scanner[host]['tcp'][port]['name']
                            host_info["ports"].append({"port": port, "service": service})
                scan_results.append(host_info)
    except Exception as e:
        scan_results.append({"error": f"Erreur lors du scan : {e}"})

    return scan_results

@staticmethod
def export_to_json(data, filename):
    """
    Exporte les données fournies dans un fichier JSON.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Les résultats ont été exportés dans le fichier : {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'exportation JSON : {e}")

@staticmethod
def ensure_file_creation(filename):
    """
    Assure la création du fichier même si les données sont vides.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump({}, json_file, ensure_ascii=False, indent=4)
        print(f"Fichier vide créé : {file_path}")
    except Exception as e:
        print(f"Erreur lors de la création du fichier vide : {e}")

if __name__ == "__main__":
print(f"Scanner Nmap - Version {NetworkScanner.VERSION}")

# Informations de la machine
machine_info = NetworkScanner.get_info_machine()
print("\nInformations de la machine :")
print(machine_info)

# Test de latence Google (une seule fois)
print("\nTest de latence vers Google...")
google_latency = NetworkScanner.test_google_latency()
if google_latency:
    print(f"Latence vers Google : {google_latency} ms")
else:
    print("Impossible de mesurer la latence vers Google.")

# Export des informations de la machine et de la latence Google
main_export_data = {
    "machine_info": machine_info,
    "google_latency": google_latency,
}
NetworkScanner.export_to_json(main_export_data, "main_results.json")

# Scan réseau sur toutes les interfaces
print("\nLancement d'un scan réseau sur toutes les interfaces...")
network_scan_results = NetworkScanner.run_nmap_scan_on_all_interfaces()
if network_scan_results:
    NetworkScanner.export_to_json(network_scan_results, "network_scan_results.json")
else:
    NetworkScanner.ensure_file_creation("network_scan_results.json")
