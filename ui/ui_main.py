import tkinter as tk

class MainApp(tk.Tk):
    # Fenetere globale avec Tkinter
    def __init__(self):
        super().__init__()
        self.title(" Harvester | client - Version DEV")
        self.geometry("700x600")
        self.configure(bg="#f0f0f0") #Définie la couleur du fond
        self.resizable(width=False, height=False) #Interdit le redimensionnement de la fenêtre

        # Ajout des widgets
        titre = tk.Label(self, text="Seahawks Harvester", bg="#f0f0f0", font=("Arial", 16, "bold"))
        titre.pack(pady=20, padx=20)



# Pour tester directement cette fenêtre en lançant ui_main.py
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
