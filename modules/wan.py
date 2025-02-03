#Fonction de latance
import subprocess
#pour windows dans result la lettre doit etre n et dans linux elle doit etre c

class WAN:
    def test_latence():
        try:
            result = subprocess.run(["ping", "-n", "1", "8.8.8.8"], capture_output=True, text=True)
            #print(result.stdout)  # Affiche la sortie du ping
            for line in result.stdout.split("\n"):
                if "temps" in line or "time=" in line:
                    return float(line.split("time=" if "time=" in line else "temps=")[1].split(" ")[0])
        except Exception as e:
            print(f"Erreur : {e}")
            return None

    latency = test_latence()
    print(f"Latence vers Google : {latency} ms" if latency else "Impossible de mesurer la latence.")