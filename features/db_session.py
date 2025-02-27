import sys
sys.dont_write_bytecode = True

import mariadb
import json

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
            database="franchise_1"
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


def insert_scan_results(results, harvester_ID):
    # envoie les resultats du scan vers la bdd
    connexion = db_connect()
    if not connexion:
        print("Impossible de se connecter à la base de données.")
        return
    
    try:
        cursor = connexion.cursor()
        

        # Convertir le dictionnaire en chaîne JSON
        scan_json_str = json.dumps(results)

        # Insère le rapport dans la colone Scan_Rapport
        query_scan = "INSERT INTO NetworkScan (Harvester_ID, Scan_Rapport) VALUES (%s, %s)"
        cursor.execute(query_scan, (harvester_ID, scan_json_str))
        connexion.commit() # Valide l'insertion

        print(f"Rapport de scan inséré avec succès sous Scan_ID={cursor.lastrowid}")

    except mariadb.Error as e:
        print(f"Erreur lors de l'insertion des résultats : {e}")

    finally:
        db_disconnect(connexion)

