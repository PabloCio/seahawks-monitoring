import tkinter as tk
from ui.ui_info import InfoFrame
from ui.ui_controls import ControlsFrame
from ui.ui_results import ResultsFrame

class MainApp(tk.Tk):
    # Fenetere globale avec Tkinter
    def __init__(self, version):
        super().__init__()
        self.title(f" Harvester | client - Version {version}")
        self.geometry("700x600")
        self.configure(bg="#f0f0f0") #Définie la couleur du fond
        self.resizable(width=False, height=False) #Interdit le redimensionnement de la fenêtre

        # Titre de MainApp
        titre = tk.Label(self, text="Seahawks Harvester", bg="#f0f0f0", font=("Arial", 16, "bold"))
        titre.pack(pady=20, padx=20)

        # Zone Info
        self.info_frame = InfoFrame(self)
        self.info_frame.pack()

        # Zone Résultat
        self.results_frame = ResultsFrame(self)
        self.results_frame.pack()

        # Zone Controle
        self.controls_frame = ControlsFrame(self, self.results_frame)
        self.controls_frame.pack()

