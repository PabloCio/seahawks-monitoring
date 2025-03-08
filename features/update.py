import os
import subprocess
import time
import requests
import threading

GITLAB_URL = os.getenv("GITLAB_URL")  # URL du dépôt GitLab
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")  # Token d'accès API GitLab
BRANCH = "main"
CHECK_INTERVAL = 86400  # Vérification toutes les 24h

def get_remote_version():
    """ Récupère la dernière version disponible sur GitLab """
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    response = requests.get(f"{GITLAB_URL}/repository/tags", headers=headers)

    if response.status_code == 200:
        latest_tag = response.json()[0]["name"]  # Récupère le dernier tag
        return latest_tag
    else:
        print(f"Erreur lors de la récupération de la version GitLab : {response.status_code}")
        return None

def update_application():
    """ Met à jour l'application si une nouvelle version est détectée """
    print("Mise à jour en cours...")
    subprocess.run(["git", "stash"])  
    subprocess.run(["git", "pull", "origin", BRANCH])  
    print("Mise à jour terminée. Redémarrage de l'application...")
    subprocess.run(["pkill", "-f", "main.py"])  
    subprocess.run(["python3", "main.py"])  

def check_for_updates(version_app):
    """ Vérifie régulièrement si une mise à jour est disponible """
    while True:
        remote_version = get_remote_version()

        if remote_version and version_app != remote_version:
            print(f"Nouvelle version détectée : {remote_version} (actuelle : {version_app})")
            update_application()
        else:
            print("Aucune mise à jour disponible.")
        
        time.sleep(CHECK_INTERVAL)

def start_update_checker(version_app):
    """ Démarre la vérification des mises à jour dans un thread séparé """
    update_thread = threading.Thread(target=check_for_updates, args=(version_app,), daemon=True)
    update_thread.start()
