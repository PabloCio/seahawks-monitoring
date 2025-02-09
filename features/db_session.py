import sys
sys.dont_write_bytecode = True

import mariadb

def db_connect():
    try:
        # Initialise la connexion à un SGBD MariaDB
        # Avec la configuration suivante
        # Seule la connexion au SGBD se fera
        # Il faudra spécifier la BDD dans une requête
        init_connexion = mariadb.connect(
            user="root",
            password="root",
            host="192.0.2.17",
            database="harverster01_db"
        )
        return init_connexion

    # Si la connexion échoue pour X raison
    except mariadb.Error as e:
        # Un message d'erreur sera afficher dans le terminal
        print(error_message = "Erreur de connexion à la base de données : {e}")

def db_disconnect(connexion): #Ferme la connexion à la base de données si ouverte
    try:
        # Si la connexion avec la BDD est initialisée 
        if connexion:
            connexion.close() #focntion qui ferme la session   
    except mariadb.Error as e:
        print(f"Erreur de déconnexion de la base de données MariaDB: {e}")


def insert_scan_results(results, franchise="default_franchise"):
    # envoie les resultats du scan vers la bdd
    connexion = db_connect()
    if not connexion:
        print("Impossible de se connecter à la base de données.")
        return
    
    try:
        cursor = connexion.cursor()

        # Insère le scan et récupérer son ID
        query_scan = "INSERT INTO Scan (franchise) VALUES (%s)"
        cursor.execute(query_scan, (franchise,))
        connexion.commit()
        id_scan = cursor.lastrowid  # Récupère l'ID du scan inséré

        # Insère les machines détectées
        query_machine = "INSERT INTO Machine (id_scan, hostname, ip_adress) VALUES (%s, %s, %s)"
        
        machine_ids = {}  # Dictionnaire pour stocker l'ID de chaque machine
        for machine in results:
            hostname = machine.get("nom_hote")
            ip_adress = machine.get("ip")

            cursor.execute(query_machine, (id_scan, hostname, ip_adress))
            connexion.commit()
            id_machine = cursor.lastrowid  # Récupère l'ID de la machine insérée
            machine_ids[ip_adress] = id_machine  # Associe l'IP à son ID machine

        # Insérer les ports ouverts pour chaque machine
        query_port = "INSERT INTO Port (id_machine, port_number) VALUES (%s, %s)"
        
        for machine in results:
            ip = machine["ip"]
            id_machine = machine_ids.get(ip)  # Récupère l'ID de la machine correspondante

            for port in machine.get("ports_ouverts", []):
                cursor.execute(query_port, (id_machine, port))
        
        connexion.commit()  # Enregistre toutes les modifications
        print(f"Scan enregistré avec id_scan={id_scan}, {len(results)} machines et leurs ports.")

    except mariadb.Error as e:
        print(f"Erreur lors de l'insertion des résultats : {e}")

    finally:
        db_disconnect(connexion)

