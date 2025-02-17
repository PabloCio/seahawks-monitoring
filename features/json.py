import json
import os

def save_scan_results(data, filename="scan_results.json"):
    """Sauvegarde les résultats du scan dans un fichier JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Résultats enregistrés dans {filename}")

def load_scan_results(filename="scan_results.json"):
    """Charge les résultats précédents du fichier JSON, ou retourne une liste vide si le fichier n'existe pas."""
    if not os.path.exists(filename):
        return []  # Aucun scan précédent
    
    with open(filename, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []  # Fichier vide ou corrompu
