import tkinter as tk

class MainApp(tk.Tk):
    """Application principale Tkinter."""
    def __init__(self):
        super().__init__()
        self.title("Seahawks Monitoring | Harvester _ Version DEV")
        self.geometry("700x600")

        # Ajout des widgets


# Pour tester directement cette fenêtre en lançant ui_main.py
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
