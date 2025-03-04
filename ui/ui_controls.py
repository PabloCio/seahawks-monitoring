import tkinter as tk
import os
from features.scan import scan_network, get_open_ports
from features.json import save_scan_results
from features.db_session import insert_scan_results
from features.system_info import get_network_range



class ControlsFrame(tk.Frame):
    def __init__(self, parent, results_frame):
        super().__init__(parent, bg="grey", height=100)
        self.pack(fill="x", padx=5, pady=5)

        self.results_frame = results_frame  # Stocke le tableau des résultats

        # Variable Tkinter pour stocker l’entrée utilisateur (modifiable)
        self.network_range_var = tk.StringVar(value=get_network_range())  # Définit la valeur initiale

        # Champ de saisie pour la plage IP (modifiable par l’utilisateur)
        self.ip_entry = tk.Entry(self, textvariable=self.network_range_var, width=20)
        self.ip_entry.pack(pady=5)

        # Bouton pour lancer le scan
        self.scan_button = tk.Button(self, text="Scan", command=self.start_scan)
        self.scan_button.pack(pady=5)

    def start_scan(self):
        """Lance le scan réseau avec la plage entrée par l'utilisateur."""

        # 1 Récupère la plage entrée par l'utilisateur
        network_range = self.network_range_var.get()
        if not network_range.strip():  # Si l'utilisateur n'a rien mis, utiliser get_network_range()
            network_range = get_network_range()

        print(f"Lancement du scan sur : {network_range}")

        # 2 On identifie les machines connectées
        machines_trouvees, devices_count = scan_network(network_range)

        print(f"Lancement du scan sur : {devices_count}")

        # 3 Charge la liste des ip des machines trouvée
        ips = [machine["ip"] for machine in machines_trouvees]

        # 4 Lancer le scan des ports ouverts
        results = get_open_ports(ips)
        if not results:
            return

        # 5 Mettre à jour l'affichage
        self.results_frame.populate_results(results)

        # 6 Sauvegarder les résultats
        save_scan_results(results)

        # 7 Enregistrer dans la base de données
        harvester_ID = int(os.getenv("HARVESTER_ID", 1))  # Charger `HARVESTER_ID` depuis `.env`
        try:
            insert_scan_results(results, harvester_ID)
        except Exception as e:
            print(f"Impossible d'envoyer les résultats en base de données : {e}")

        # 8 Met à jour le nombre de machine dans le dashboard