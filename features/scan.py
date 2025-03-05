import nmap
from features.system_info import get_network_range, get_local_ip, get_hostname, get_wan_latency

def scan_network(network_range=None, fast=False):
    """
    Scanne les machines connectées au réseau.
    :param network_range: Plage réseau sous forme '192.168.1.0/24'. Si None, utilise get_network_range().
    :param fast: Si True, ne récupère que les IPs sans chercher les noms d'hôte.
    :return: Tuple (Liste des machines trouvées, Nombre total de machines)
    """
    if network_range is None:
        network_range = get_network_range()  # On récupère la plage réseau automatiquement

    scanner = nmap.PortScanner()
    scan_type = "Scan RAPIDE (uniquement comptage des machines)" if fast else "Scan COMPLET (détails et ports ouverts)"
    print(f" {scan_type} sur {network_range}...")

    try:
        scanner.scan(hosts=network_range, arguments="-sn", timeout=20)

        machines_trouvees = []
        for host in scanner.all_hosts():
            nom_hote = scanner[host].hostname() or "Inconnu" if not fast else "?"
            machines_trouvees.append({"ip": host, "nom_hote": nom_hote})

        return machines_trouvees, len(machines_trouvees)

    except Exception as e:
        print(f"Erreur lors du scan : {e}")
        return [], 0

def get_open_ports(ips, ports="1-1000"):
    """
    Effectue un scan des ports ouverts uniquement sur les machines identifiées.
    :param ips: Liste d'IP des machines détectées.
    :param ports: Plage de ports à scanner.
    :return: Liste des machines avec leurs ports ouverts.
    """
    scanner = nmap.PortScanner()
    print(f"Scan des ports ouverts sur {len(ips)} machines...")

    results = []
    try:
        for ip in ips:
            print(f"Scan des port {ip}")

            scanner.scan(hosts=ip, arguments=f"-p {ports} -T4 -sS", timeout=20)

            nom_hote = scanner[ip].hostname() or "Inconnu"
            ports_ouverts = [
                port for port, infos in scanner[ip].get("tcp", {}).items() if infos["state"] == "open"
            ]

            results.append({
                "ip": ip,
                "nom_hote": nom_hote,
                "ports_ouverts": ports_ouverts
            })

        return results

    except Exception as e:
        print(f"Erreur lors du scan des ports : {e}")
        return []
    
def get_system_info():
    """
    Récupère toutes les informations système en une seule fois :
    - Hostname
    - IP locale
    - Latence WAN
    - Nombre de machines connectées
    """
    hostname = get_hostname()
    local_ip = get_local_ip()
    latency = get_wan_latency()
    _, device_count = scan_network(get_network_range(), fast=True)

    return {
        "hostname": hostname,
        "local_ip": local_ip,
        "latency": latency,
        "device_count": device_count
    }     
    