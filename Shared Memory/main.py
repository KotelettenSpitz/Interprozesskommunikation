import time, subprocess, os, sys

# Liste der Dateien, die ausgeführt werden sollen
Dateien = ["Conv.py", "Log.py", "Stat.py", "Report.py"]

# Der Pfad des aktuellen Verzeichnisses, in dem sich das Skript befindet
folder_path = os.path.dirname(__file__)

# Funktion zum Ausführen einer Datei
def run_file(file_name):
    # Farbcode für die Ausgabe
    Farbe = ["\033[92m"]
    Standardfarbe = "\033[0m"
    # Ausgabe einer Nachricht, dass die Datei ausgeführt wird
    print(f"{Farbe[os.getpid() % len(Farbe)]}Ausführen von {file_name}...{Standardfarbe}", flush=True)
    # Ausführen der Datei
    subprocess.run(["/usr/bin/python3", file_name], stdout=sys.stdout)

# Hauptschleife zum Erstellen von Kindprozessen und Ausführen der Dateien
for Datei_Name in Dateien:
    pid = os.fork()  # Erstellen eines neuen Prozesses
    if pid == 0:  # Wenn im Kindprozess
        run_file(Datei_Name)  # Datei ausführen
        exit()  # Kindprozess beenden
    time.sleep(0.75)  # Warten, bevor der nächste Prozess erstellt wird

# Warten, bis alle Kindprozesse beendet sind
for _ in range(len(Dateien)):
    os.wait()  # Warten auf einen Kindprozess
