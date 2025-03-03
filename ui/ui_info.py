import tkinter as tk
from features.system_info import get_hostname, get_local_ip, get_wan_latency, get_network_range
from features.scan import scan_network

class InfoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="grey", height=100)
        self.pack(fill="x", padx=5, pady=5)

        # Création des Labels
        self.hostname_label = tk.Label(self, text="Hostname : Chargement…", bg="grey", fg="black", font=("Arial", 12))
        self.hostname_label.pack()

        self.local_ip_label = tk.Label(self, text="Adresse IP : Chargement…", bg="grey", fg="black", font=("Arial", 12))
        self.local_ip_label.pack()

        self.latency_label = tk.Label(self, text="Latence : Calcul en cours…", bg="grey", fg="black", font=("Arial", 12))
        self.latency_label.pack()

        self.device_count_label = tk.Label(self, text="Machines connectées : Chargement…", bg="grey", fg="black", font=("Arial", 12))
        self.device_count_label.pack()

        # Lancer la mise à jour des infos après affichage
        self.after(100, self.update_info)

    def update_info(self):
        """Met à jour les informations après l'affichage."""
        hostname = get_hostname()
        local_ip = get_local_ip()
        latency = get_wan_latency()
        _, device_count = scan_network(get_network_range(), fast=True)

        # Déterminer la couleur en fonction de la latence
        latency_color = "grey"
        if latency is not None:
            if latency < 50:
                latency_color = "green"
            elif latency < 150:
                latency_color = "orange"
            else:
                latency_color = "red"

        # Mettre à jour les Labels
        self.hostname_label.config(text=f"Hostname : {hostname}")
        self.local_ip_label.config(text=f"Adresse IP : {local_ip}")
        self.latency_label.config(text=f"Latence : {latency} ms", bg=latency_color)
        self.device_count_label.config(text=f"Machines connectées : {device_count}")

        self.after(300000, self.update_info)
