import subprocess
import tkinter as tk
from ui.ui_main import MainApp

VERSION = "0.2"

def check_for_updates():
    """Vérifie si une mise à jour est disponible."""
    try:
        output = subprocess.check_output(["git", "pull"], text=True)
        if "Already up to date" not in output:
            print("Une mise à jour est disponible ! Redémarrage en cours.")
    except Exception as e:
        print(f"Erreur lors de la vérification des mises à jour : {e}")

if __name__ == "__main__":
    check_for_updates()
    app = MainApp(VERSION)
    app.mainloop()
