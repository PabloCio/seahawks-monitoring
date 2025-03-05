import tkinter as tk
from features.scan import get_system_info
from features.db_session import update_harvester_dashboard

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

        # Lancer la mise à jour des infos système
        self.after(100, self.update_info)

    def update_info(self):
        """Met à jour les informations après l'affichage."""
        system_info = get_system_info()

        # Déterminer la couleur en fonction de la latence
        latency_color = "grey"
        if system_info["latency"] is not None:
            if system_info["latency"] < 50:
                latency_color = "green"
            elif system_info["latency"] < 150:
                latency_color = "orange"
            else:
                latency_color = "red"

         # Mettre à jour les Labels avec les nouvelles informations
        self.hostname_label.config(text=f"Hostname : {system_info['hostname']}")
        self.local_ip_label.config(text=f"Adresse IP : {system_info['local_ip']}")
        self.latency_label.config(text=f"Latence : {system_info['latency']} ms", bg=latency_color)
        self.device_count_label.config(text=f"Machines connectées : {system_info['device_count']}")

        # Lancer également la mise à jour de la base de données
        update_harvester_dashboard(system_info, self.master.version)

        self.after(300000, self.update_info)  # Rafraîchit toutes les 5 minutes
        print(" Update dashboard terminé")
