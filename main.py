import tkinter as tk
from front import Dashboard # Import classe Dashboard



# Point d'entrée principal
if __name__ == "__main__":
    main_windows = tk.Tk()  # Crée la fenêtre principale

    # Initialise le dashboard
    app = Dashboard(main_windows)

    # Lancement de l'application
    main_windows.mainloop()