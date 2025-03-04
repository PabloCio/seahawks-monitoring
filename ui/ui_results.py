import tkinter as tk
from tkinter import ttk  # Tkinter Treeview
from features.json import save_scan_results, load_scan_results

#Zone affichant les résultats du scan sous forme de tableau

class ResultsFrame(tk.Frame): 
    def __init__(self, parent):
        super().__init__(parent, bg="yellow", height=300)
        self.pack(fill="both", expand=True, padx=5, pady=5)

        # Création du Tableau via Treeview
        self.tree = ttk.Treeview(self, columns=("Hostname", "IP", "Ports"), show="headings")

        # Colonnes
        self.tree.heading("Hostname", text="Hostname")
        self.tree.heading("IP", text="Adresse IP")
        self.tree.heading("Ports", text="Ports ouverts")

        # Largeurs des colonnes
        self.tree.column("Hostname", width=150)
        self.tree.column("IP", width=120)
        self.tree.column("Ports", width=200)

        # Ajout d'un scrollbar vertical
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Placement du Treeview et du scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Chargement des résultats précédents
        previous_results = load_scan_results()
        self.populate_results(previous_results)

    def populate_results(self, data):
        """Ajoute des résultats dans le tableau et les sauvegarde."""
        self.tree.delete(*self.tree.get_children())  # Efface les anciennes entrées

        for machine in data:
            hostname = machine.get("nom_hote","Inconnu")  # Indique que hostname doit être le "nom_hote" ou "Inconnu"
            ip = machine.get("ip", "Indisponible")
            open_ports = machine.get("ports_ouverts", [])
            open_ports_str = ", ".join(map(str, open_ports)) if open_ports else "Aucun"

            self.tree.insert("", "end", values=(hostname, ip, open_ports_str))