
# Class pour les fonctions boutons
class Backend:

    # fonction scan réseau
    def lancer_scan(self):
        print("Scan réseau lancé !")
        # données fictives
        self.lastest_scan_results = [
            {"hostname": "Device 1", "ip": "192.168.1.11", "ports": "22, 80, 443"},
            {"hostname": "Device 2", "ip": "192.168.1.12", "ports": "21, 22, 3306"},
            {"hostname": "Device 3", "ip": "192.168.1.13", "ports": "22, 8080, 8443"},
        ]
        print("Scan terminé !", self.lastest_scan_results),

    # fonction vérification de la version
    def check_update(self):
        print("Vérification des mises à jour...")
        # Résultat fictif
        self.update_status = "Votre application est à jour."
        print(self.update_status)