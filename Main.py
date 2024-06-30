import os
import time
import signal
import TCP
import MessageQueues
import PipesKelvin
import Conv
import Log
import Stat
import Report
import sys

# Hauptprogramm
if __name__ == "__main__":

    # Signal-Handler für SIGINT (z.B. Strg+C)
    def signal_handler(signum, frame):
        print("\nBeende das Programm...")
        # Sendet SIGTERM an alle Kindprozesse, um sie zu beenden
        for pid in ProzessIDs:
            os.kill(pid, signal.SIGTERM)
        sys.exit()

    # Funktion zum Starten eines neuen Prozesses
    def prozess_starten(prozess):
        pid = os.fork()  # Erstellt einen neuen Prozess
        if pid == 0:  # Kindprozess
            prozess()  # Führt die übergebene Funktion im Kindprozess aus
            os._exit(0)  # Beendet den Kindprozess nach Ausführung der Funktion
        return pid  # Gibt die PID des Kindprozesses im Elternprozess zurück

    # Benutzeraufforderung zur Auswahl der Implementierungsvariante
    print("Message Queues: M")
    print("Pipes: P")
    print("Shared Memory: S")
    print("TCP: T")

    input = input("Wählen sie ihre Implementierungsvariante: ")

    # Wenn eine gültige Auswahl getroffen wurde
    if input == "T" or input == "S" or input == "M" or input == "P" or input == "t" or input == "s" or input == "m" or input == "p" :
        # Tabellenüberschrift und Design für die Ausgabe
        spalten = ["Zeit", "Summe", "Mittelwert"]
        design = "+" + "+".join(["-" * (len(col) + 2) for col in spalten]) + "+"

        # Tabellenüberschrift ausgeben
        print(design)
        print("|", end="")
        for col in spalten:
            print(f" {col} |", end="")
        print("\n" + design)
 
    ProzessIDs = []  # Liste zum Speichern der PIDs der gestarteten Prozesse

    # Startet die entsprechenden Prozesse basierend auf der Auswahl des Benutzers
    if input == "T" or input == "t":
        ProzessIDs.append(prozess_starten(TCP.conv_process))
        ProzessIDs.append(prozess_starten(TCP.log_process))
        ProzessIDs.append(prozess_starten(TCP.stat_process))
        ProzessIDs.append(prozess_starten(TCP.report_process))

    elif input == "M" or input == "m":
        ProzessIDs.append(prozess_starten(MessageQueues.conv_process))
        ProzessIDs.append(prozess_starten(MessageQueues.log_process))
        ProzessIDs.append(prozess_starten(MessageQueues.stat_process))
        ProzessIDs.append(prozess_starten(MessageQueues.report_process))

    elif input == "P" or input == "p":
        ProzessIDs.append(prozess_starten(PipesKelvin.conv_process))
        ProzessIDs.append(prozess_starten(PipesKelvin.log_process))
        ProzessIDs.append(prozess_starten(PipesKelvin.stat_process))
        ProzessIDs.append(prozess_starten(PipesKelvin.report_process))

    elif input == "S" or input == "s":
        ProzessIDs.append(prozess_starten(Conv.conv_process))
        ProzessIDs.append(prozess_starten(Log.log_process))
        ProzessIDs.append(prozess_starten(Stat.stat_process))
        ProzessIDs.append(prozess_starten(Report.report_process))
    
    else:
        # Wenn eine ungültige Eingabe gemacht wurde
        print("Eingabe nicht erkannt")
        sys.exit()

    # Setzt den Signal-Handler für SIGINT (z.B. Strg+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Hält den Hauptprozess am Laufen, bis ein SIGINT empfangen wird
    while True:
        time.sleep(1)

