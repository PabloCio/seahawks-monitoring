import tkinter as tk
from features.scan import get_open_ports
from features.json import save_scan_results


class ControlsFrame(tk.Frame):
    # Zone contenant les boutons et la saisie de l'IP
    def __init__(self, parent, results_frame):
        super().__init__(parent, bg="grey", height=100)
        self.pack(fill="x", padx=5, pady=5)

        # Stockage du tableau des résultats pour l'update
        self.results_frame = results_frame 

        # Variable Tkinter pour stocker l’entrée utilisateur
        self.ip_entry_var = tk.StringVar()
        # Champ de saisie pour la plage IP
        self.ip_entry = tk.Entry(self, textvariable=self.ip_entry_var, width=20)
        self.ip_entry.pack(pady=5)

        # Bouton pour lancer le scan
        self.scan_button = tk.Button(self, text="Scan", command=self.start_scan)
        self.scan_button.pack(pady=5)
    
    def start_scan(self):
        """Lance le scan réseau et met à jour le tableau des résultats."""
        network_range = self.ip_entry_var.get()  # Récupère la plage entrée
        if not network_range:
            print("Erreur : veuillez entrer une plage réseau.")
            return
        
        # Lancer le scan
        results = get_open_ports(network_range)

        # Mettre à jour le tableau
        self.results_frame.populate_results(results)

        # Sauvegarder les résultats du scan
        save_scan_results(results)
        