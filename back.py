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
            return (hostname, local_ip, Backend.VERSION)
        except socket.error as e:
            return ("Erreur", f"Erreur : {e}", Backend.VERSION)

    @staticmethod
    def get_nbr_machines():
        """
        Retourne un nombre fictif de machines connectées pour l'affichage.
        """
        try:
            return len(psutil.net_if_addrs())
        except Exception as e:
            return f"Erreur : {str(e)}"

    @staticmethod
    def test_wan_latency(label):
        """
        Teste la latence vers Google et met à jour un label Tkinter avec le résultat.
        """
        def update_label():
            try:
                result = subprocess.run(
                    ["ping", "-n", "1", "8.8.8.8"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.returncode == 0 and result.stdout:
                    for line in result.stdout.splitlines():
                        if "temps" in line or "time" in line:
                            latency_part = line.split("temps=" if "temps" in line else "time=")[1]
                            latency = latency_part.split("ms")[0].strip()
                            label.config(text=f"Latence WAN : {latency} ms")
                            return
                label.config(text="Latence WAN : Non mesurable")
            except Exception as e:
                label.config(text=f"Erreur de latence : {str(e)}")

        # Appel de la mise à jour dans un thread séparé pour éviter de bloquer l'interface
        label.after(100, update_label)

    @staticmethod
    def lancer_scan():
        """
        Effectue un scan réseau rapide sur le sous-réseau local et retourne les résultats.
        """
        scanner = nmap.PortScanner()
        subnet = "192.168.1.0/24"  # Par défaut, un sous-réseau local
        results = []

        try:
            scanner.scan(hosts=subnet, arguments="-F")  # Scan rapide (-F)
            for host in scanner.all_hosts():
                hostname = scanner[host].hostname() or "Nom de machine inconnu"
                state = scanner[host].state()
                open_ports = []

                if 'tcp' in scanner[host]:
                    for port in sorted(scanner[host]['tcp']):
                        if scanner[host]['tcp'][port]['state'] == 'open':
                            service = scanner[host]['tcp'][port]['name']
                            open_ports.append(f"{port}/{service}")

                results.append((hostname, host, ", ".join(open_ports)))
        except Exception as e:
            results.append((f"Erreur : {str(e)}", "N/A", "N/A"))

        return results

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
