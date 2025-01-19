import subprocess
import socket
import psutil
import nmap

VERSION = "1.2"

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
                    ip_list.append((address.address, iface_name))
        return ip_list
    except Exception as e:
        return [("Erreur : Non disponible", str(e))]

def test_latency(site):
    """
    Teste la latence d'un site donné et retourne le temps moyen en millisecondes.
    """
    try:
        result = subprocess.run(
            ["ping", "-n", "1", site],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='cp850',
            errors="replace"  # Remplace les caractères non décodables
        )
        if result.stdout:
            for line in result.stdout.splitlines():
                if "temps" in line or "time" in line:
                    latency_part = line.split("temps=" if "temps" in line else "time=")[1]
                    latency = latency_part.split("ms")[0].strip()
                    return int(latency)
        return None
    except Exception as e:
        print(f"Erreur lors du test de latence pour {site} : {e}")
        return None

def calculate_average_latency():
    """
    Calcule la latence moyenne entre Google et Orange.
    """
    sites = ["google.com", "orange.fr"]
    latencies = []
    for site in sites:
        latency = test_latency(site)
        if latency is not None:
            latencies.append(latency)

    if latencies:
        average_latency = sum(latencies) / len(latencies)
        print(f"Latence moyenne entre {', '.join(sites)} : {average_latency:.2f} ms")
    else:
        print("Impossible de calculer la latence moyenne.")

def run_nmap_scan_on_all_interfaces():
    """
    Lance un scan Nmap rapide (-F) sur toutes les interfaces réseau détectées.
    Affiche uniquement les ports ouverts et le nom de la machine.
    """
    scanner = nmap.PortScanner()
    local_ips = get_all_local_ips()

    for ip, iface in local_ips:
        print(f"\nScan rapide de l'interface {iface.encode('utf-8', errors='replace').decode()} (IP : {ip})...")
        try:
            scanner.scan(hosts=ip, arguments="-F")  # Option rapide pour Nmap
            for host in scanner.all_hosts():
                hostname = scanner[host].hostname() or "Nom de machine inconnu"
                print(f"\nRésultats pour {host} ({hostname}):")
                print(f"État : {scanner[host].state()}")
                if 'tcp' in scanner[host]:
                    for port in sorted(scanner[host]['tcp']):
                        if scanner[host]['tcp'][port]['state'] == 'open':
                            service = scanner[host]['tcp'][port]['name']
                            print(f"Port {port}/tcp : ouvert ({service})")
        except Exception as e:
            print(f"Erreur lors du scan de {iface}: {e}")

if __name__ == "__main__":
    print(f"Scanner Nmap - Version {VERSION}")
    print("\nCalcul de la latence moyenne...")
    calculate_average_latency()
    print("\nLancement du scan rapide sur toutes les interfaces réseau...")
    run_nmap_scan_on_all_interfaces()
