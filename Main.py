import os
import time
import signal
import sys
import TCP
import MessageQueues
import PipesKelvin

if __name__ == "__main__":
    
    def signal_handler_TCP(signum, frame):
        print("\nBeende das Programm...")
        for pid in ProzessIDs:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                continue
        for pid in ProzessIDs:
            try:
                os.waitpid(pid, 0)
            except ChildProcessError:
                continue
            for sock in [TCP.server1, TCP.server2, TCP.client, TCP.server, TCP.server3, TCP.client3]:
                try:
                    sock.close()
                except Exception:
                    continue
            sys.exit(0)

    def signal_handler_MQ(signum, frame):
        print("\nBeende das Programm...")
        for pid in ProzessIDs:
            os.kill(pid, signal.SIGTERM)
        for name in ["/mq1", "/mq2", "/mq3"]:
            MessageQueues.DeleteQueue(name)
        os._exit(0)

    def signal_handler_Pipes(signum, frame):
        print("\nBeende das Programm...")
        for pid in ProzessIDs:
            os.kill(pid, signal.SIGTERM)
        PipesKelvin.entfernen_pipes()
        os._exit(0)

    print("Message Queues: M")
    print("Pipes: P")
    print("Shared Memory: S")
    print("TCP: T")

    input = input("Wählen sie ihre Implementierungsvariante: ")

#------------------------------------------------------------------------------------------------------  

    if input == "M":
        MessageQueues.CreateQueue()
    
    if input == "P":
        PipesKelvin.benannte_pipes()

    ProzessIDs = []
    
    ProzessIDs.append(os.fork())
    if ProzessIDs[-1] == 0:
        if input == "T":
            TCP.conv_process()
        elif input == "M":
            MessageQueues.conv_process()
        elif input == "P":
            PipesKelvin.conv_process()
        os._exit(0)

    if input == "T":
        time.sleep(5)

    ProzessIDs.append(os.fork())
    if ProzessIDs[-1] == 0:
        if input == "T":
            TCP.log_process()
        elif input == "M":
            MessageQueues.log_process() 
        elif input == "P":
            PipesKelvin.log_process()
        os._exit(0)
    
    ProzessIDs.append(os.fork())
    if ProzessIDs[-1] == 0:
        if input == "T":
            TCP.stat_process()
        elif input == "M":
            MessageQueues.stat_process()    
        elif input == "P":
            PipesKelvin.stat_process()        
        os._exit(0)

    if input == "T":
        time.sleep(5)

    ProzessIDs.append(os.fork())
    if ProzessIDs[-1] == 0:
        if input == "T":
            TCP.report_process()
        elif input == "M":
            MessageQueues.report_process() 
        elif input == "P":
            PipesKelvin.report_process()
        os._exit(0)

    signal.signal(signal.SIGINT, signal_handler_TCP)
    
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            if input == "T":
                signal_handler_TCP(signal.SIGINT, None)
            elif input == "M":
                signal_handler_MQ(signal.SIGINT, None)
            elif input == "P":
                signal_handler_Pipes(signal.SIGINT, None)
