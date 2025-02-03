# Vérification des outils et installation
import subprocess
import sys

def install_and_import(*packages):
        # Vérifie si un ou plusieurs modules sont installés. Si non, les installe via pip.
        for package in packages:
            try:
                __import__(package)
                print(f"{package} est déjà installé.")
            except ImportError:
                print(f"{package} n'est pas installé. Installation en cours...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    __import__(package)  # Réessaye d'importer après installation
                    print(f"{package} a été installé avec succès.")
                except Exception as e:
                    print(f"Échec de l'installation de {package} : {e}")

# Installation des modules nécessaires
install_and_import("python-nmap", "netifaces")

# Vérification que nmap est installé sur la machine
try:
    result = subprocess.run(['nmap', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("nmap est installé :", result.stdout.splitlines()[0])
except Exception:
    print("nmap n'est pas installé ou n'est pas accessible en ligne de commande. Veuillez l'installer manuellement.")
    sys.exit(1)