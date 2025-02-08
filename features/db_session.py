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

        # Renvoie la configuration de connexion
        return init_connexion

    # Si la connexion échoue pour X raison
    except mariadb.Error as e:
        # Un message d'erreur sera afficher dans le terminal
        print(error_message = "Erreur de connexion à la base de données : {e}")

def db_disconnect():
    try:
        # Si la connexion avec la BDD est initialisée 
        if db_connect():

            # On ferme la connexion
            db_connect().close()

    # En cas d'erreur            
    except mariadb.Error as e:
        print(f"Erreur de déconnexion de la base de données MariaDB: {e}")


def db_get_table(nom_table):
    try:
        cur = db_connect().cursor()
        mareq = f"SELECT * FROM {nom_table}"
        cur.execute(mareq)
        resultats = cur.fetchall()
        return resultats
    except mariadb.DatabaseError as e:
        print(f"Impossible de récupérer les données: {e}")
        return None
    
# Exemple d'utilisation :
table = "Scan"
resultats_db = db_get_table(table)

# Affichage des résultats
if resultats_db:
    for ligne in resultats_db:
        print(ligne)
else:
    print("Aucune donnée récupérée.")