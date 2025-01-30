import tkinter as tk
from tkinter import ttk  # Import Tkinter pour créer des interfaces graphiques
from back import Backend  # Backend à connecter à ta logique

class Dashboard:
    def __init__(self, main_windows):
        # Initialise la fenêtre principale
        self.main_window = main_windows
        self.main_window.title(f"Seahawks Monitoring | Harvester - {Backend.get_info_machine()[2]}")  # Titre de la fenêtre
        self.main_window.geometry("700x600")  # Définit la taille de la fenêtre en pixels

        # Configure les widgets
        self.setup_ui()

        # Affiche les dernière données de scan
        self.display_data()

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
        top_frame.pack(pady=20)  # Ajoute un espace vertical autour des cadres

        # Données fictives pour l'affichage
        hostname_label = tk.Label(top_frame, text=f"Hostname : {Backend.get_info_machine()[0]}", font=("Helvetica", 12))
        hostname_label.grid(row=0, column=0, padx=10, pady=5)

        devices_label = tk.Label(top_frame, text=f"Machines connectées : {Backend.get_nbr_machines()}", font=("Helvetica", 12))
        devices_label.grid(row=0, column=1, padx=10, pady=5)

        ip_label = tk.Label(top_frame, text=f"Adress IP : {Backend.get_info_machine()[1]}", font=("Helvetica", 12))
        ip_label.grid(row=1, column=0, padx=10, pady=5)

        self.latency_label = tk.Label(top_frame, text="Latence WAN : En cours...", font=("Helvetica", 12))
        self.latency_label.grid(row=1, column=1, padx=10, pady=5)

        # Lancer la fonction pour mettre à jour la latence WAN
        Backend.test_wan_latency(self.latency_label)

    def add_bouton_frame(self):
        # Ajoute la section bouton (central)
        bouton_frame = tk.Frame(self.main_window)
        bouton_frame.pack(pady=20)

        # Bouton pour lancer actualisé
        scan_button = tk.Button(bouton_frame, text="Actualiser l'interface", font=("Helvetica", 12), command=Backend.get_info_machine)
        scan_button.grid(row=0, column=0, padx=10, pady=5)

        # Bouton pour lancer un scan
        scan_button = tk.Button(bouton_frame, text="Lancer un scan", font=("Helvetica", 12), command=self.display_data)
        scan_button.grid(row=0, column=1, padx=10, pady=5)

        # Bouton de mise à jour
        scan_button = tk.Button(bouton_frame, text="Vérification de la version", font=("Helvetica", 12), command=self.display_data)
        scan_button.grid(row=0, column=2, padx=10, pady=5)

        # Ajoute le titre principal "Seahawks Monitoring"
        title_update = tk.Label(bouton_frame, text="A jour", font=("Helvetica", 10, "bold"))
        title_update.grid(row=0, column=3, padx=10, pady=5)

    def display_data(self): #afficher les resultat du scan
        data = Backend.lancer_scan() #Appelle les données

        # Efface les données précédentes dans le tableau
        for item in self.scan_table.get_children():
            self.scan_table.delete(item)

        # Ajoute les nouvelles données dans le tableau
        for pc, ip, ports in data:
            self.scan_table.insert("", tk.END, values=(pc, ip, ports))

    def add_scan_frame(self):
        # Ajoute la section pour afficher les données du scan
        scan_frame = tk.Frame(self.main_window, relief="groove", borderwidth=2)
        scan_frame.pack(pady=20, fill="x")

        # Titre du cadre SCAN
        scan_title = tk.Label(scan_frame, text="Résultats du dernier scan réseau", font=("Helvetica", 14, "bold"))
        scan_title.pack(pady=10)

        # Création du tableau Treeview
        columns = ("Host", "IP Address", "Ports")
        self.scan_table = ttk.Treeview(scan_frame, columns=columns, show="headings", height=10)
        self.scan_table.pack(fill=tk.BOTH, expand=True)

        # Configuration des colonnes
        self.scan_table.heading("Host", text="Host")
        self.scan_table.heading("IP Address", text="IP Address")
        self.scan_table.heading("Ports", text="Ports")