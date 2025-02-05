import tkinter as tk
from tkinter import ttk  # Tkinter Treeview

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

        # Ajout de quelques résultats fictifs
        self.populate_results([
            {"hostname": "PC-1", "ip": "192.168.1.10", "ports": [22, 80]},
            {"hostname": "PC-2", "ip": "192.168.1.12", "ports": [3389]},
            {"hostname": "PC-3", "ip": "192.168.1.15", "ports": []},  # Aucun port ouvert
        ])

    def populate_results(self, data):
        """Ajoute des résultats dans le tableau."""
        self.tree.delete(*self.tree.get_children())  # Efface les anciennes entrées

        for machine in data:
            hostname = machine["hostname"]
            ip = machine["ip"]
            open_ports = ", ".join(map(str, machine["ports"])) if machine["ports"] else "Aucun"

            self.tree.insert("", "end", values=(hostname, ip, open_ports))