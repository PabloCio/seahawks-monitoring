import subprocess
import tkinter as tk
import os
from ui.ui_main import MainApp
from features.update import start_update_checker

VERSION_APP = "0.3"

if __name__ == "__main__":
    start_update_checker(VERSION_APP)
    app = MainApp(VERSION_APP)
    app.mainloop()
