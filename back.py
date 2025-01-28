import socket
import psutil
import subprocess
import nmap
import json
import os


class Backend:
    VERSION = "1.3"

    @staticmethod
    def get_info_machine():
        """
        Retourne les informations de la machine locale : hostname, IP locale et version de l'application.
        """
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            version = Backend.VERSION
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
    def lancer_scan():
        """
        Effectue un scan réseau sur toutes les interfaces réseau.
        """
        scanner = nmap.PortScanner()
        ip_list = Backend.get_all_local_ips()
        scan_results = []

        try:
            for ip_info in ip_list:
                ip = ip_info["ip"]
                subnet = f"{ip}/24"  # Sous-réseau à scanner
                scanner.scan(hosts=subnet, arguments="-F")  # Scan rapide (-F) du sous-réseau
                for host in scanner.all_hosts():
                    hostname = scanner[host].hostname() or "Nom de machine inconnu"
                    state = scanner[host].state()
                    ports = []
                    if 'tcp' in scanner[host]:
                        for port in sorted(scanner[host]['tcp']):
                            if scanner[host]['tcp'][port]['state'] == 'open':
                                ports.append({"port": port, "service": scanner[host]['tcp'][port]['name']})
                    scan_results.append({
                        "host": host,
                        "hostname": hostname,
                        "state": state,
                        "ports": ports
                    })
        except Exception as e:
            scan_results.append({"error": f"Erreur lors du scan : {e}"})

        return scan_results

    @staticmethod
    def test_wan_latency(label):
        """
        Met à jour la latence vers Google dans un label donné.
        """
        latency = Backend.test_google_latency()
        if latency:
            label.config(text=f"Latence WAN : {latency} ms")
        else:
            label.config(text="Latence WAN : Erreur")
