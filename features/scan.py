import nmap

def get_open_ports(network_range, ports="1-1000"):
    """
    Effectue un scan réseau sur une plage d'IP donnée.
    
    :param network_range: La plage d'IP à scanner (ex: "192.168.1.0/24")
    :param ports: Plage de ports à scanner (par défaut : tous les ports)
    :return: Liste des machines trouvées avec IP, nom d'hôte et ports ouverts
    """
    scanner = nmap.PortScanner()
    print(f" Scan en cours sur {network_range}...")
    
    try:
        scanner.scan(hosts=network_range, arguments=f"-p {ports} -T4 -sS")

        resultats = []
        for host in scanner.all_hosts():
            nom_hote = scanner[host].hostname() or "Inconnu"
            ports_ouverts = []

            if "tcp" in scanner[host]:
                for port, infos in scanner[host]["tcp"].items():
                    if infos["state"] == "open":
                        ports_ouverts.append(port)

            resultats.append({
                "ip": host,
                "nom_hote": nom_hote,
                "ports_ouverts": ports_ouverts
            })

        return resultats

    except Exception as e:
        print(f" Erreur lors du scan : {e}")
        return []

#  Exemple d'utilisation :
#plage = "192.168.1.0/24"  # Modifie selon ton réseau
#resultats_scan = get_open_portsk(plage)

# Affichage des résultats
#for machine in resultats_scan:
    #print(f"{machine['ip']} ({machine['nom_hote']}) - Ports ouverts : {machine['ports_ouverts']}")

def scan_network(network_range):
    """
    Détecte les machines connectées sur une plage d'IP sans scanner les ports.
    
    :param network_range: La plage d'IP à scanner (ex: "192.168.1.0/24")
    :return: Liste des machines trouvées avec IP et nom d'hôte
    """
    scanner = nmap.PortScanner()
    print(f" Scan des machines connectées sur {network_range}...")

    try:
        scanner.scan(hosts=network_range, arguments="-sn")  # Scan sans ports (-sn)

        machines_trouvees = []
        for host in scanner.all_hosts():
            nom_hote = scanner[host].hostname() or "Inconnu"
            machines_trouvees.append({"ip": host, "nom_hote": nom_hote})

        return machines_trouvees

    except Exception as e:
        print(f" Erreur lors du scan : {e}")
        return []

#  Exemple d'utilisation :
#plage = "192.168.1.0/24"  # Modifie selon ton réseau
#resultats = scan_network(plage)

 #Affichage des résultats
#for machine in resultats:
    #print(f"{machine['ip']} ({machine['nom_hote']})")
