import tkinter as tk

class MainApp(tk.Tk):
    #Application principale Tkinter
    def __init__(self):
        super().__init__()
        self.title("Seahawks Monitoring | Harvester - Version DEV") # Titre de la fenêtre
        self.geometry("700x600") # Définit la taille de la fenêtre en pixels

        # Ajout des widgets
        

# Pour tester directement cette fenêtre en lançant ui_main.py
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
