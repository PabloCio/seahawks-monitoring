import tkinter as tk
from ui.ui_info import InfoFrame
from ui.ui_controls import ControlsFrame
from ui.ui_results import ResultsFrame
from features.json import load_scan_results  # Charger les derniers résultats du scan

class MainApp(tk.Tk):
    def __init__(self, version):
        super().__init__()
        self.version = version # Stocke la version dans l'instance de l'application

        self.title(f"Harvester | Client - Version {self.version}")
        self.geometry("700x600")
        self.configure(bg="#f0f0f0")
        self.resizable(width=False, height=False)

        # Titre de l'application
        self.titre = tk.Label(self, text="Seahawks Harvester", bg="#f0f0f0", font=("Arial", 16, "bold"))
        self.titre.pack(pady=20)

        # Zone Info (IP locale, hostname, latence, nombre de machines)
        self.info_frame = InfoFrame(self)
        self.info_frame.pack()

        # Zone Résultats (Tableau des scans)
        self.results_frame = ResultsFrame(self)
        self.results_frame.pack()

        # Zone Contrôle (Boutons de scan)
        self.controls_frame = ControlsFrame(self, self.results_frame)
        self.controls_frame.pack()

        # Charger les derniers résultats du scan depuis JSON sans refaire un scan
        self.load_last_scan()

    def load_last_scan(self):
        """Charge les derniers résultats du scan depuis JSON et les affiche."""
        last_results = load_scan_results()
        self.results_frame.populate_results(last_results)  # Affichage sans relancer un scan