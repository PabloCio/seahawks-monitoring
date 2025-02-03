import tkinter as tk

from tkinter import ttk

class Dashboard:
    def __init__(self, main_windows): # Initialise la fenêtre principale
        self.main_window = main_windows
        self.main_window.title(f"Seahawks Monitoring | Harvester - ") # Titre de la fenêtre
        self.main_window.geometry("700x600") # Définit la taille de la fenêtre en pixels

        # Configure les widgets
        self.setup_ui()

    def setup_ui(self):
        # Mise en place des sections de l'interface
        self.add_title()
        self.add_top_frame()
        self.add_bouton_frame()
        self.add_scan_frame()

    def add_title(self):
        # Ajoute le titre principal "Seahawks Monitoring"
        title_label = tk.Label(self.main_window, text="Seahawks Monitoring", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

    def add_top_frame(self):
        # Ajoute la section supérieure
        top_frame = tk.Frame(self.main_window)
        top_frame.pack(pady=20) # Ajoute un espace vertical autour des cadres

        # Affiche le Hsotname
        hostname_label = tk.Label(top_frame, text=f"Hostname : ", font=("Helvetica", 12))
        hostname_label.grid(row=0, column=0, padx=10, pady=5)
        # Affiche nbr Machines connectées
        self.devices_label = tk.Label(top_frame, text=f"Machines connectées : ", font=("Helvetica", 12))
        self.devices_label.grid(row=0, column=1, padx=10, pady=5)
        # Affiche l'adresses IP de la machine
        ip_label = tk.Label(top_frame, text=f"Adresse IP : ", font=("Helvetica", 12))
        ip_label.grid(row=1, column=0, padx=10, pady=5)
        # Affiche la latence WAN
        self.latency_label = tk.Label(top_frame, text=f"Latence WAN : ", font=("Helvetica", 12))
        self.latency_label.grid(row=1, column=1, padx=10, pady=5)

    def add_bouton_frame(self):
        # Ajoute une section bouton
        bouton_frame = tk.Frame(self.main_window)
        bouton_frame.pack(pady=20)

        # Bouton pour lancer actualisé
        scan_button = tk.Button(bouton_frame, text="Actualiser l'interface", font=("Helvetica", 12))
        scan_button.grid(row=0, column=0, padx=10, pady=5)

        # Bouton pour lancer un scan
        scan_button = tk.Button(bouton_frame, text="Lancer un scan", font=("Helvetica", 12))
        scan_button.grid(row=0, column=1, padx=10, pady=5)

        # Bouton de mise à jour
        scan_button = tk.Button(bouton_frame, text="Vérification de la version", font=("Helvetica", 12))
        scan_button.grid(row=0, column=2, padx=10, pady=5)

        # Ajoute l'indication pour la version
        title_update = tk.Label(bouton_frame, text="A jour", font=("Helvetica", 10, "bold"))
        title_update.grid(row=0, column=3, padx=10, pady=5)

    def add_scan_frame(self):
        # Ajoute la section pour afficher les données du scan
        scan_frame = tk.Frame(self.main_window, relief="groove", borderwidth=2)
        scan_frame.pack(pady=20, fill="x")

        # Titre du cadre SCAN
        scan_title = tk.Label(scan_frame, text="Résultats du dernier scan réseau", font=("Helvetica", 14, "bold"))
        scan_title.pack(pady=10)

        # Création du tableau Treeview
        columns = ("IP", "Hostname", "Ports")
        self.scan_table = ttk.Treeview(scan_frame, columns=columns, show="headings", height=10)
        self.scan_table.pack(fill=tk.BOTH, expand=True)

        # Configuration des colonnes
        for col in columns:
            self.scan_table.heading(col, text=col)
