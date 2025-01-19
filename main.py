import tkinter as tk
from front import Dashboard # Import classe Dashboard
from back import Backend # Import classe Backend


# Point d'entrée principal
if __name__ == "__main__":
    main_windows = tk.Tk()  # Crée la fenêtre principale

    # Initialisation des fonctionnalités back-end
    backend = Backend()

    # Initialise le dashboard
    app = Dashboard(main_windows)

    # Lancement de l'application
    main_windows.mainloop()