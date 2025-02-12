import tkinter as tk


from features.system_info import get_hostname, get_local_ip, get_wan_latency, get_connected_devices_count

class InfoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="grey", height=100)
        self.pack(fill="x", padx=5, pady=5)

        # Récuparation des infos système
        hostname = get_hostname()
        local_ip = get_local_ip()
        latency = get_wan_latency()
        count = get_connected_devices_count(f"{local_ip}/24")

        # Création des Labels
        self.hostname_label = tk.Label(self, text=f"Hostname : {hostname}", bg="grey", fg="black", font=("Arial", 12))
        self.hostname_label.pack()

        self.local_ip_label = tk.Label(self, text=f"Adresse IP : {local_ip}", bg="grey", fg="black", font=("Arial", 12))
        self.local_ip_label.pack()

        self.latency_label = tk.Label(self, text=f"Latence : {latency}", bg="grey", fg="black", font=("Arial", 12))
        self.latency_label.pack()

        self.count_label = tk.Label(self, text=f"Nombre de machines : {count}", bg="grey", fg="black", font=("Arial", 12))
        self.count_label.pack()