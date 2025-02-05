import tkinter as tk
import socket

def get_hostname():
    return socket.gethostname()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # Se connecte au DNS de Google pour déterminer l'IP locale
    ip_locale = s.getsockname()[0]
    s.close()
    return ip_locale

class InfoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="grey", height=100)
        self.pack(fill="x", padx=5, pady=5)

        # Récuparation des infos système
        hostname = get_hostname()
        local_ip = get_local_ip()

        # Création des Labels
        self.hostname_label = tk.Label(self, text=f"Hostname : {hostname}", bg="grey", fg="black", font=("Arial", 12))
        self.hostname_label.pack()

        self.local_ip_label = tk.Label(self, text=f"Adresse IP : {local_ip}", bg="grey", fg="black", font=("Arial", 12))
        self.local_ip_label.pack()