import tkinter as tk  # Import Tkinter pour créer des interfaces graphiques


class Dashboard:
    def __init__(self, main_windows):
        # Initialise la fenêtre principale
        self.main_window = main_windows
        self.main_window.title("Seahawks Monitoring | Harvester - Version Dev")  # Titre de la fenêtre
        self.main_window.geometry("700x600")  # Définit la taille de la fenêtre en pixels

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
        top_frame.pack(pady=20)  # Ajoute un espace vertical autour des cadres

        # Données fictives pour l'affichage
        hostname_label = tk.Label(top_frame, text="Hostname : Harvester-Montpellier", font=("Helvetica", 12))
        hostname_label.grid(row=0, column=0, padx=10, pady=5)

        devices_label = tk.Label(top_frame, text="Machines connectées : 5", font=("Helvetica", 12))
        devices_label.grid(row=0, column=1, padx=10, pady=5)

        ip_label = tk.Label(top_frame, text="Adress IP : 192.168.1.10", font=("Helvetica", 12))
        ip_label.grid(row=1, column=0, padx=10, pady=5)

        latence_label = tk.Label(top_frame, text="Latence WAN : 32ms", font=("Helvetica", 12))
        latence_label.grid(row=1, column=1, padx=10, pady=5)

    def add_bouton_frame(self):
        # Ajoute la section bouton (central)
        bouton_frame = tk.Frame(self.main_window)
        bouton_frame.pack(pady=20)

        # Bouton pour vérifier les mises à jour
        update_button = tk.Button(bouton_frame, text="Vérifier les mises à jour", font=("Helvetica", 12))
        update_button.grid(row=0, column=0, padx=10, pady=5)

        # Bouton pour lancer un scan
        scan_button = tk.Button(bouton_frame, text="Lancer un scan", font=("Helvetica", 12))
        scan_button.grid(row=0, column=1, padx=10, pady=5)

    def add_scan_frame(self):
        # Ajoute la section pour afficher les données du scan
        scan_frame = tk.Frame(self.main_window, relief="groove", borderwidth=2)
        scan_frame.pack(pady=20, fill="x")

        # Titre du cadre SCAN
        scan_title = tk.Label(scan_frame, text="Résultats du dernier scan réseau", font=("Helvetica", 14, "bold"))
        scan_title.pack(pady=10)

        # Scan fictif
        device1 = tk.Label(scan_frame, text="Hostname : Device 1 | Adresse IP : 192.168.1.11 | Ports ouvert : 22, 80, 443", font=("Helvetica", 12))
        device1.pack(padx=10, pady=5)

        device2 = tk.Label(scan_frame, text="Hostname : Device 2 | Adresse IP : 192.168.1.12 | Ports ouvert : 21, 22, 3306", font=("Helvetica", 12))
        device2.pack(padx=10, pady=5)

        device3 = tk.Label(scan_frame, text="Hostname : Device 3 | Adresse IP : 192.168.1.13 | Ports ouvert : 22, 8080, 8443", font=("Helvetica", 12))
        device3.pack(padx=10, pady=5)