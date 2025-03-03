# ui_main.py
import tkinter as tk
from tkinter import ttk

class HarvesterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Harvester - Scan Réseau")
        self.geometry("700x500")
        
        self.create_widgets()

    def create_widgets(self):
        # Section des informations système
        info_frame = ttk.Frame(self)
        info_frame.pack(pady=10, fill="x")

        ttk.Label(info_frame, text="Hostname: SERV-01").pack(side="left", padx=10)
        ttk.Label(info_frame, text="IP: 192.168.1.100").pack(side="left", padx=10)
        ttk.Label(info_frame, text="Latence WAN: 15ms").pack(side="left", padx=10)
        ttk.Label(info_frame, text="Machines connectées: 5").pack(side="left", padx=10)
        
        # Frame pour les actions de scan et mise à jour
        scan_frame = ttk.Frame(self)
        scan_frame.pack(pady=10, fill="x", padx=10)

        self.scan_button = ttk.Button(scan_frame, text="Lancer le Scan")
        self.scan_button.pack(side="left", padx=10)
        
        self.ip_entry = ttk.Entry(scan_frame, width=20)
        self.ip_entry.insert(0, "192.168.1.0/24")
        self.ip_entry.pack(side="left", padx=10)
        
        self.update_button = ttk.Button(scan_frame, text="Mettre à jour Infos")
        self.update_button.pack(side="left", padx=10)
        
        self.tree = ttk.Treeview(self, columns=("IP", "Hostname", "Ports"), show="headings")
        self.tree.heading("IP", text="Adresse IP")
        self.tree.heading("Hostname", text="Nom d'hôte")
        self.tree.heading("Ports", text="Ports ouverts")
        self.tree.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = HarvesterApp()
    app.mainloop()
