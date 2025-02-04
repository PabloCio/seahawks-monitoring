import tkinter as tk
from ui.ui_info import InfoFrame
from ui.ui_controls import ControlsFrame
from ui.ui_results import ResultsFrame

class MainApp(tk.Tk):
    # Fenetere globale avec Tkinter
    def __init__(self):
        super().__init__()
        self.title(" Harvester | client - Version DEV")
        self.geometry("700x600")
        self.configure(bg="#f0f0f0") #Définie la couleur du fond
        self.resizable(width=False, height=False) #Interdit le redimensionnement de la fenêtre

        # Titre de MainApp
        titre = tk.Label(self, text="Seahawks Harvester", bg="#f0f0f0", font=("Arial", 16, "bold"))
        titre.pack(pady=20, padx=20)

        # Ajout de la zone Info
        self.info_frame = InfoFrame(self)
        self.info_frame.pack()

        # Ajout de la zone Controle
        self.controls_frame = ControlsFrame(self)
        self.controls_frame.pack()

         # Ajout de la zone Résultat
        self.results_frame = ResultsFrame(self)
        self.results_frame.pack()

# Pour tester directement cette fenêtre en lançant ui_main.py
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
