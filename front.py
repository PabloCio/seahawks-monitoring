import tkinter as tk #Import Tkinter module pour créer des interface graphique

class Dashboard:
    def __init__(self, main_windows):

        # Initialise la fenetre principale
        self.main_window = main_windows
        self.main_window.title("Seahawks Monitoring | Harvester - Version Dev") # Titre de la fenêtre
        self.main_window.geometry("800x600") # Defini la taille de la fenêtre en pixels

        # Configure les widgets
        self.setup_ui()

    def setup_ui(self):

        # Ajout d'un titre
        title_label = tk.Label(self.main_window, text='Seahawks Monitoring', font=("Helvetica",16, "bold"))
        title_label.pack(pady=10)

        # Interface TOP
        top_frame = tk.Frame(self.main_window)
        top_frame.pack(pady=20) # Ajoute un espace vertical autour des cadres

        # Premier cadre carré
        left_square = tk.Frame(top_frame, width=340, height=150, relief="solid", borderwidth=2)
        left_square.grid(row=0, column=0, padx=10)  # Place le cadre à gauche
        left_square.pack_propagate(False)  # Désactive l'ajustement automatique à son contenu

        # Données fictives pour l'affichage
        hostname_label = tk.Label(left_square, text="Hostname : Harvester-Montpellier", font=("Helvetica", 12), anchor="w")
        hostname_label.pack(fill="both", padx=10, pady=5)

        ip_label = tk.Label(left_square, text="Adress IP : 192.168.1.10", font=("Helvetica", 12), anchor="w")
        ip_label.pack(fill="both", padx=10, pady=5)

        latence_label = tk.Label(left_square, text="Latence WAN : 32ms", font=("Helvetica", 12), anchor="w")
        latence_label.pack(fill="both", padx=10, pady=5)

        devices_label = tk.Label(left_square, text="Machines connectées : 5", font=("Helvetica", 12), anchor="w")
        devices_label.pack(fill="both", padx=10, pady=5)

        # Deuxième cadre carré
        right_square = tk.Frame(top_frame, width=340, height=150, relief="solid", borderwidth=2)
        right_square.grid(row=0, column=1, padx=10)  # Place le cadre à droite
        right_square.pack_propagate(False)  # Désactive l'ajustement automatique à son contenu

        # Données fictives pour l'affichage
        version_label = tk.Label(right_square, text="Version Dev", font=("Helvetica", 12), anchor="w")
        version_label.pack(fill="both", padx=10, pady=5)

        # Bouton pour vérifier les mises à jour
        update_button = tk.Button(right_square, text="Vérifier la version", font=("Helvetica", 12), anchor="w")
        update_button.pack(fill="both", padx=10, pady=5)

        # Bouton pour lancer un scan
        scan_button = tk.Button(right_square, text="Scan", font=("Helvetica", 12), anchor="w")
        scan_button.pack(fill="both", padx=10, pady=5)

        # Ajout cadre pour résultat du dernier scan
        scan_frame = tk.Frame(self.main_window, relief="groove", borderwidth=2) #cadre avec bordure visualisé
        scan_frame.pack(pady=20, fill="x") # Remplit horizontalement la fenêtre

        # Titre du cadre SCAN
        scan_title = tk.Label(scan_frame, text="Résultats du dernier scan réseau", font=("Helvetica", 14, "bold"))
        scan_title.pack(pady=10)

        # Ajout d'une grille pour afficher les données du scan
        header_scan_frame = tk.Frame(scan_frame)
        header_scan_frame.pack()

        # Scan fictif
        device1 = tk.Label(header_scan_frame, text="Hostname : Device 1 | Adresse IP : 192.168.1.11 | Ports ouvert : 22, 80, 443", font=("Helvetica", 12))
        device1.grid(row=0, column=0, padx=10, pady=5)

        device2 = tk.Label(header_scan_frame, text="Hostname : Device 2 | Adresse IP : 192.168.1.12 | Ports ouvert : 21, 22, 3306", font=("Helvetica", 12))
        device2.grid(row=1, column=0, padx=10, pady=5)

        device3 = tk.Label(header_scan_frame, text="Hostname : Device 3 | Adresse IP : 192.168.1.13 | Ports ouvert : 22, 8080, 8443", font=("Helvetica", 12))
        device3.grid(row=2, column=0, padx=10, pady=5)

       