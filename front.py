import tkinter as tk
from tkinter import ttk
import threading
from back import Backend  # Backend à connecter à la logique


class Dashboard:
    def __init__(self, main_windows):
        self.main_window = main_windows
        self.main_window.title(f"Seahawks Monitoring | Harvester - {Backend.VERSION}")
        self.main_window.geometry("700x600")

        self.setup_ui()

    def setup_ui(self):
        self.add_title()
        self.add_top_frame()
        self.add_bouton_frame()
        self.add_scan_frame()

    def add_title(self):
        title_label = tk.Label(self.main_window, text="Seahawks Monitoring", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

    def add_top_frame(self):
        top_frame = tk.Frame(self.main_window)
        top_frame.pack(pady=20)

        machine_info = Backend.get_info_machine()

        hostname_label = tk.Label(top_frame, text=f"Hostname : {machine_info['hostname']}", font=("Helvetica", 12))
        hostname_label.grid(row=0, column=0, padx=10, pady=5)

        self.devices_label = tk.Label(top_frame, text="Machines connectées : En attente", font=("Helvetica", 12))
        self.devices_label.grid(row=0, column=1, padx=10, pady=5)

        ip_label = tk.Label(top_frame, text=f"Adresse IP : {machine_info['local_ip']}", font=("Helvetica", 12))
        ip_label.grid(row=1, column=0, padx=10, pady=5)

        self.latency_label = tk.Label(top_frame, text="Latence WAN : En cours...", font=("Helvetica", 12))
        self.latency_label.grid(row=1, column=1, padx=10, pady=5)

        Backend.test_wan_latency(self.latency_label)

    def add_bouton_frame(self):
        bouton_frame = tk.Frame(self.main_window)
        bouton_frame.pack(pady=20)

        scan_button = tk.Button(
            bouton_frame, text="Lancer un scan", font=("Helvetica", 12), command=self.start_scan_thread)
        scan_button.grid(row=0, column=0, padx=10, pady=5)

    def add_scan_frame(self):
        scan_frame = tk.Frame(self.main_window, relief="groove", borderwidth=2)
        scan_frame.pack(pady=20, fill="x")

        scan_title = tk.Label(scan_frame, text="Résultats du dernier scan réseau", font=("Helvetica", 14, "bold"))
        scan_title.pack(pady=10)

        columns = ("Host", "Hostname", "State", "Ports")
        self.scan_table = ttk.Treeview(scan_frame, columns=columns, show="headings", height=10)
        self.scan_table.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            self.scan_table.heading(col, text=col)

    def start_scan_thread(self):
        """
        Lance le scan réseau dans un thread séparé.
        """
        self.scan_table.delete(*self.scan_table.get_children())  # Efface les données précédentes
        self.devices_label.config(text="Machines connectées : En cours...")  # Mise à jour du label
        threading.Thread(target=self.display_data, daemon=True).start()

    def display_data(self):
        """
        Exécute le scan réseau et met à jour le tableau machine par machine.
        """
        scan_results = Backend.lancer_scan()

        machine_count = 0
        for result in scan_results:
            host = result["host"]
            hostname = result["hostname"]
            state = result["state"]
            ports = ", ".join([f"{p['port']}/{p['service']}" for p in result["ports"]])

            # Ajout de la machine dans le tableau
            self.scan_table.insert("", tk.END, values=(host, hostname, state, ports))

            # Mise à jour du compteur de machines
            machine_count += 1
            self.devices_label.config(text=f"Machines connectées : {machine_count}")

        # Fin du scan
        self.devices_label.config(text=f"Scan terminé : {machine_count} machines détectées.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()
