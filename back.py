import socket
import psutil
import subprocess
import time
import threading
# Class pour les fonctions boutons

class Backend:

    @staticmethod # Fonction pour obtenir les informations de la machine locale
    def get_info_machine():
        try:
            hostname = socket.gethostname() # Identifie le hsotname
            local_ip = socket.gethostbyname(hostname) # Identifie l'IP local
            version = "DEV 1.0"  # Version de l'application
            return hostname, local_ip, version # hostname = 0, ip = 1, version = 3
        except socket.error as e:
            return f"Erreur : {e}", None
      
    @staticmethod # Fonction pour tester la latence WAN - besoin de import subprocess
    def test_wan_latency(latency_label):
        def run():
            while True:
                try:
                    result = subprocess.run(["ping", "-n", "1", "8.8.8.8"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if result.returncode == 0:
                        output = result.stdout
                        if "Average" in output:
                            latency = output.split("Average = ")[1].split("ms")[0].strip()
                        elif "Moyenne" in output:
                            latency = output.split("Moyenne = ")[1].split("ms")[0].strip()
                        else:
                            latency = "Format inconnu"
                        latency_label.config(text=f"Latence WAN : {latency} ms")
                    else:
                        latency_label.config(text="Latence WAN : Inaccessible")
                except Exception as e:
                    latency_label.config(text="Erreur : Latence WAN")
                time.sleep(60)  # 1 minutes

        threading.Thread(target=run, daemon=True).start()

    # fonction scan réseau
    @staticmethod
    def lancer_scan():
        # Exemple de données fictives pour un scan réseau
        scan_results = [
            ("PC01", "192.168.1.3", "22, 80"),
            ("PC02", "192.168.1.5", "20, 443"),
            ("PC03", "192.168.1.9", "26, 88"),
            ("PC04", "192.168.1.12", "10, 80")
        ]

        return scan_results
    
    # fonction scan réseau
    @staticmethod
    def get_nbr_machines():
        # Exemple de données fictives pour un scan réseau
        scan_results = [
            ("PC01", "192.168.1.3", "22, 80"),
            ("PC02", "192.168.1.5", "20, 443"),
            ("PC03", "192.168.1.9", "26, 88"),
            ("PC04", "192.168.1.12", "10, 80")
        ]

        nbr_machines = len(scan_results)
        return nbr_machines
    