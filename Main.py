import os
import time
import signal
import TCP
import MessageQueues
import PipesKelvin

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

#------------------------------------------------------------------------------------------------------  
    ProzessIDs = []
    
    if input == "T":
        ProzessIDs.append(prozess_starten(TCP.conv_process))
        ProzessIDs.append(prozess_starten(TCP.log_process))
        ProzessIDs.append(prozess_starten(TCP.stat_process))
        ProzessIDs.append(prozess_starten(TCP.report_process))

    if input == "M":
        ProzessIDs.append(prozess_starten(MessageQueues.conv_process))
        ProzessIDs.append(prozess_starten(MessageQueues.log_process))
        ProzessIDs.append(prozess_starten(MessageQueues.stat_process))
        ProzessIDs.append(prozess_starten(MessageQueues.report_process))

    if input == "P":
        ProzessIDs.append(prozess_starten(PipesKelvin.conv_process))
        ProzessIDs.append(prozess_starten(PipesKelvin.log_process))
        ProzessIDs.append(prozess_starten(PipesKelvin.stat_process))
        ProzessIDs.append(prozess_starten(PipesKelvin.report_process))

    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        time.sleep(1)
