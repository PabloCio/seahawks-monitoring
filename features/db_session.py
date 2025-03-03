import sys
sys.dont_write_bytecode = True

import mariadb
import json
import os

from dotenv import load_dotenv
from pathlib import Path
from features.system_info import get_hostname, get_local_ip, get_wan_latency, get_network_range
from features.scan import scan_network

def db_connect():
    try:
        return mariadb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME")
        )
    except mariadb.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")

def db_disconnect(connexion):
    """Ferme la connexion à la base de données si elle est ouverte."""
    try:
        if connexion:
            connexion.close()
    except mariadb.Error as e:
        print(f"Erreur de déconnexion : {e}")

def update_harvester_dashboard(harvester_ID=None):
    """Met à jour les informations du Harvester dans la base de données."""
    print("Mise à jour du Harvester dans la base de données...")

    dotenv_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=dotenv_path, override=True)

    if harvester_ID is None:
        harvester_ID = int(os.getenv("HARVESTER_ID"))

    connexion = db_connect()
    if not connexion:
        print("Impossible de se connecter à la base de données.")
        return
    
    try:
        cursor = connexion.cursor()

        hostname = get_hostname()  
        local_ip = get_local_ip()  
        wan_latency = get_wan_latency()
        harvester_version = os.getenv("HARVESTER_VERSION", "1.0")
        network_range = get_network_range()  #On utilise toujours la plage réseau du Harvester
        _, machines_count = scan_network(network_range, fast=True)  # Scan rapide


        sql = """
        INSERT INTO Harvester (Harvester_ID, Harvester_IP, Harvester_Hostname, Harvester_Version, Harvester_WAN, Machine_Count)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Harvester_IP = VALUES(Harvester_IP),
            Harvester_Hostname = VALUES(Harvester_Hostname),
            Harvester_Version = VALUES(Harvester_Version),
            Harvester_WAN = VALUES(Harvester_WAN),
            Machine_Count = VALUES(Machine_Count);
        """
        cursor.execute(sql, (harvester_ID, local_ip, hostname, harvester_version, wan_latency, machines_count))
        connexion.commit()

        print("Mise à jour effectuée avec succès.")

    except mariadb.Error as e:
        print(f"Erreur lors de l'insertion : {e}")

    finally:
        db_disconnect(connexion)

def insert_scan_results(results, harvester_ID=None): # envoie les infos du harvester vers la bdd
    # Charge .env 
    dotenv_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=dotenv_path, override=True)
    print(f"DB_HOST={os.getenv('DB_HOST')}, DB_USER={os.getenv('DB_USER')}, DB_PASSWORD={os.getenv('DB_PASSWORD')}, DB_NAME={os.getenv('DB_NAME')}")

    # Si harvester_ID n'est pas défini, le charger depuis .env
    if harvester_ID is None:
        harvester_ID = int(os.getenv("HARVESTER_ID"))
    
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