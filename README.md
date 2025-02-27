# Harvester

Application Python MSPR

Harvester est une application Python permettant de scanner un réseau, identifier les machines connectées et analyser leurs ports ouverts. Les résultats sont affichés dans une interface graphique, sont sauvegardés localement et dans une base de données MariaDB.

# Structure du Projet

/SRC #Contient les fichiers Python principaux
README.md
requirements.txt
.env
main.py

/SRC/UI #Contient les fichiers liés à l'interface graphique Tkinter

ui_controls.py → Gère les boutons et interactions de l’interface graphique
ui_info.py → Affiche les informations système dans l’interface
ui_main.py → Fichier principal qui initialise et affiche la fenêtre principale de l’application
ui_results.py → Gère l’affichage des résultats des scans dans le tableau Treeview


/SRC/FEATURES #Contient les fonctionnalités de l'app

db_session.py → Gère la connexion et les interactions avec la base de données MariaDB
json.py → Gère l'enregistrement et la lecture des résultats des scans en JSON
scan.py → Effectue le scan du réseau et détecte les machines connectées ainsi que leurs ports ouverts
system_info.py → Récupère les informations système comme l’IP locale, le hostname et la latence WAN
update.py → Vérifie les mises à jour de l’application sur GitLab et permet la mise à jour automatique

# Installation

Installer : Python et pip
Installer les dépendances avec : pip install -r requirements.txt
Configurer le fichier .env en indiquant les infromations de connection pour la BDD

# Utilisation

Exécuter le programme avec : python main.py

# Auteurs

Nicolas
Adil
Jeremy
Pablo
