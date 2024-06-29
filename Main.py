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

if __name__ == "__main__":

    def signal_handler(signum, frame):
        print("\nBeende das Programm...")
        for pid in ProzessIDs:
            os.kill(pid, signal.SIGTERM)
        os._exit(0)

    def prozess_starten(prozess):
        pid = os.fork()
        if pid == 0:
            prozess()
            os._exit(0)
        return pid

    print("Message Queues: M")
    print("Pipes: P")
    print("Shared Memory: S")
    print("TCP: T")

    input = input("Wählen sie ihre Implementierungsvariante: ")

    if input == "T" or input == "S" or input == "M" or input == "P":
        # Tabellenüberschrift und Design für die Ausgabe
        spalten = ["Zeit", "Summe", "Mittelwert"]
        design = "+" + "+".join(["-" * (len(col) + 2) for col in spalten]) + "+"

        # Tabellenüberschrift ausgeben
        print(design)
        print("|", end="")
        for col in spalten:
            print(f" {col} |", end="")
        print("\n" + design)
 
    ProzessIDs = []

    if input == "T":
        ProzessIDs.append(prozess_starten(TCP.conv_process))
        ProzessIDs.append(prozess_starten(TCP.log_process))
        ProzessIDs.append(prozess_starten(TCP.stat_process))
        ProzessIDs.append(prozess_starten(TCP.report_process))

    elif input == "M":
        ProzessIDs.append(prozess_starten(MessageQueues.conv_process))
        ProzessIDs.append(prozess_starten(MessageQueues.log_process))
        ProzessIDs.append(prozess_starten(MessageQueues.stat_process))
        ProzessIDs.append(prozess_starten(MessageQueues.report_process))

    elif input == "P":
        ProzessIDs.append(prozess_starten(PipesKelvin.conv_process))
        ProzessIDs.append(prozess_starten(PipesKelvin.log_process))
        ProzessIDs.append(prozess_starten(PipesKelvin.stat_process))
        ProzessIDs.append(prozess_starten(PipesKelvin.report_process))

    elif input == "S":
        ProzessIDs.append(prozess_starten(Conv.conv_process))
        ProzessIDs.append(prozess_starten(Log.log_process))
        ProzessIDs.append(prozess_starten(Stat.stat_process))
        ProzessIDs.append(prozess_starten(Report.report_process))
    
    else:
        print("Eingabe nicht erkannt")
        exit()

    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        time.sleep(1)
