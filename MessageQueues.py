import time
import random
import posix_ipc
import struct

def conv_process():
    mq1 = posix_ipc.MessageQueue("/mq1", flags=posix_ipc.O_CREAT, mode=0o600, max_messages=10, max_message_size=1024) #Message Queues erstellen
    mq2 = posix_ipc.MessageQueue("/mq2", flags=posix_ipc.O_CREAT, mode=0o600, max_messages=10, max_message_size=1024)
    try:
        while True: #Schleife um Prozess endlos laufen zu lassen
            value = random.randint(0, 1023) #Zufallszahl erstellen
            if value <= 1023 and value >= 0:
                SendToQueue("/mq1", value, None) #Wert an Queues senden
                SendToQueue("/mq2", value, None)
            time.sleep(1)
    finally:
        mq1.unlink() #Bei Prozessende Message Queues löschen
        mq2.unlink()

def log_process():
    with open('log.txt', 'a') as log: #Log Datei öffnen
        try:
            while True:
                value = ReceiveFromQueue("/mq1") #Daten Empfangen
                log.write(f"{value}\n") #Wert in Datei schreiben
                log.flush() #Sofortiges schreiben erzwingen
        finally:
            pass

def stat_process():
    mq3 = posix_ipc.MessageQueue("/mq3", flags=posix_ipc.O_CREAT, mode=0o600, max_messages=10, max_message_size=1024) #Message Queue erstellen
    values = [] #Array erstellen
    try:
        while True: #Schleife um Prozess endlos laufen zu lassen
            value = ReceiveFromQueue("/mq2") #Daten Empfangen
            if value is not None: #Wenn Wert übergeben
                values.append(value) #Wert zum Array hinzufügen
                sum_values = sum(values) #Summe errechnen
                average = sum(values) / len(values) #Mittelwert errechnen
                SendToQueue("/mq3", sum_values, average) #Daten an Queue senden
                time.sleep(1)
    finally:
        mq3.unlink() #Bei Prozessende Message Queue löschen

def report_process():
    try:
        while True: #Schleife um Prozess endlos laufen zu lassen
            sum_values, average = ReceiveFromQueue("/mq3") #Daten Empfangen
            if sum_values is not None and average is not None: #Wenn Daten empfangen
                print(f"| {time.strftime('%H:%M:%S')} | {sum_values} | {average} |") #Daten ausgeben
            time.sleep(1)
    finally:
        pass

def SendToQueue(name, value, value2):
    mq = posix_ipc.MessageQueue(name) #Message Queue auswählen
    if name == "/mq1" or name == "/mq2": #Wenn /mq1 oder /mq2 da hier nur ein Datenwert übergeben wird
        mq.send(struct.pack('i', value), 0) #Daten senden und konvertieren
    elif name == "/mq3": #Wenn /mq3, da hier zwei Datenwerte übergeben werden
        mq.send(struct.pack('2i', value, int(value2)), 0) #Daten senden und konvertieren

def ReceiveFromQueue(name):
    mq = posix_ipc.MessageQueue(name) #Message Queue auswählen
    if name == "/mq1" or name == "/mq2": #Wenn /mq1 oder /mq2 da hier nur ein Datenwert empfangen wird
        prevalue, _ = mq.receive() #Daten empfangen
        value = struct.unpack('i', prevalue)[0] #Daten konvertieren
        return value #Daten zurückgeben
    elif name == "/mq3": #Wenn /mq3, da hier ein Datenwert übergeben wird
        message, _ = mq.receive(timeout=1) #Daten empfangen
        sum_values, average = struct.unpack('2i', message) #Daten konvertieren
        return sum_values, average #Daten zurückgeben