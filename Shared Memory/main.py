import time, subprocess, os, sys

Dateien = ["Conv.py", "Log.py", "Stat.py", "Report.py"]

folder_path = os.path.dirname(__file__)

def run_file(file_name):
    Farbe = ["\033[92m"]
    Standardfarbe = "\033[0m"
    print(f"{Farbe[os.getpid() % len(Farbe)]}Ausführen von {file_name}...{Standardfarbe}", flush=True)
    subprocess.run(["/usr/bin/python3", file_name], stdout=sys.stdout)
    print(f"{Farbe[os.getpid() % len(Farbe)]}{file_name} wurde ausgeführt.{Standardfarbe}", flush=True)

for Datei_Name in Dateien:
    pid = os.fork()
    if pid == 0:
        run_file(Datei_Name)
        exit()
    time.sleep(0.75)

for _ in range(len(Dateien)):
    os.wait()