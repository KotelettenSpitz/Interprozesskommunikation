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

    if input == "T":
        ProzessIDs = []
    
        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            TCP.conv_process()
            os._exit(0)

        time.sleep(5)

        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            TCP.log_process()
            os._exit(0)
    
        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            TCP.stat_process()
            os._exit(0)

        time.sleep(5)
    
        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            TCP.report_process()
            os._exit(0)

        signal.signal(signal.SIGINT, signal_handler_TCP)
    
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                signal_handler_TCP(signal.SIGINT, None)

#------------------------------------------------------------------------------------------------------               

    elif input == "M":
        MessageQueues.CreateQueue()

        ProzessIDs = []
    
        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            MessageQueues.conv_process()
            os._exit(0)

        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            MessageQueues.log_process()
            os._exit(0)
    
        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            MessageQueues.stat_process()
            os._exit(0)
    
        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            MessageQueues.report_process()
            os._exit(0)

        signal.signal(signal.SIGINT, signal_handler_TCP)
    
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                signal_handler_MQ(signal.SIGINT, None)

#------------------------------------------------------------------------------------------------------ 
    elif input == "P":

        ProzessIDs = []
    
        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            PipesKelvin.conv_process()
            os._exit(0)

        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            PipesKelvin.log_process()
            os._exit(0)
    
        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            PipesKelvin.stat_process()
            os._exit(0)
    
        ProzessIDs.append(os.fork())
        if ProzessIDs[-1] == 0:
            PipesKelvin.report_process()
            os._exit(0)

        signal.signal(signal.SIGINT, signal_handler_Pipes)
    
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                signal_handler_Pipes(signal.SIGINT, None)
