import tkinter as tk

class ResultsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="grey", height=100)
        self.pack(fill="x", padx=5, pady=5)

        # Ajout d'un texte pour tester l'affichage
        label = tk.Label(self, text="Zone Résultats Système", bg="grey", fg="black", font=("Arial", 12))
        label.pack(pady=10)