import tkinter as tk

class ControlsFrame(tk.Frame):
    # Zone contenant les boutons et la saisie de l'IP
    def __init__(self, parent):
        super().__init__(parent, bg="grey", height=100)
        self.pack(fill="x", padx=5, pady=5)

        # Variable Tkinter pour stocker l’entrée utilisateur
        self.ip_entry_var = tk.StringVar()

        # Champ de saisie pour la plage IP
        self.ip_entry = tk.Entry(self, textvariable=self.ip_entry_var, width=20)
        self.ip_entry.pack(pady=5)

        # Bouton pour lancer le scan
        self.scan_button = tk.Button(self, text="Scan", command=self.start_scan)
        self.scan_button.pack(pady=5)
    
    def start_scan(self):
        """Affiche temporairement la plage IP entrée."""
        print(f"Scan lancé sur : {self.ip_entry_var.get()}")
        