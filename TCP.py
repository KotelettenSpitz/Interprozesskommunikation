import socket
import random
import time
import struct

# Funktion für den Erzeugerprozess
def conv_process():
    # Erstellt zwei TCP-Sockets für die Server
    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bindet die Sockets an lokale Adressen und Ports
    server1.bind(('localhost', 9999))
    server2.bind(('localhost', 9998))
    
    # Lauscht auf eingehende Verbindungen
    server1.listen(1)
    server2.listen(1)
    
    # Akzeptiert eingehende Verbindungen
    client_socket1, addr = server1.accept()
    client_socket2, addr = server2.accept()

    try:
        while True: #Schleife zum endlosen ausführen des Prozesses
            # Generiert eine Zufallszahl zwischen 1 und 100
            prevalue = random.randint(1, 100)
            # Verpackt die Zahl als 4-Byte-Integer
            value = struct.pack('i', prevalue)
            # Sendet die Zahl an beide Clients
            client_socket1.sendall(value)
            client_socket2.sendall(value)
            # Wartet eine Sekunde
            time.sleep(1)
    finally:
        # Schließt die Server-Sockets
        server1.close()
        server2.close()

# Funktion für den Logging-Prozess
def log_process():
    # Erstellt einen TCP-Client-Socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Verbindet sich zum Server auf Port 9999
    while True:
        try:
            client.connect(('localhost', 9999))
            break
        except ConnectionRefusedError:
            # Falls die Verbindung fehlschlägt, versucht es erneut nach einer Sekunde
            time.sleep(1)
            continue
    
    try:
        while True: #Schleife zum endlosen ausführen des Prozesses
            # Empfängt 4 Bytes vom Server
            data = client.recv(4)
            # Entpackt die empfangene Zahl
            value = struct.unpack('i', data)[0]
            # Schreibt die Zahl in die Logdatei
            with open("log.txt", "a") as log:
                log.write(str(value) + "\n")
                log.flush()
    finally:
        # Schließt den Client-Socket
        client.close()

# Funktion für den Statistikprozess
def stat_process():
    # Erstellt einen TCP-Client-Socket und einen weiteren Server-Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Verbindet sich zum Server auf Port 9998
    while True:
        try:
            server.connect(('localhost', 9998))
            break
        except ConnectionRefusedError:
            # Falls die Verbindung fehlschlägt, versucht es erneut nach einer Sekunde
            time.sleep(1)
            continue
    
    # Bindet den zweiten Server-Socket an eine lokale Adresse und einen Port
    server3.bind(('localhost', 9996))
    # Lauscht auf eingehende Verbindungen
    server3.listen(1)
    # Akzeptiert eine eingehende Verbindung
    client_socket, addr = server3.accept()

    values = []
    try:
        while True: #Schleife zum endlosen ausführen des Prozesses
            # Empfängt 4 Bytes vom Server
            data = server.recv(4)
            # Entpackt die empfangene Zahl
            value = struct.unpack('i', data)[0]
            values.append(value)
            # Berechnet den Durchschnitt der empfangenen Zahlen
            average = sum(values) // len(values)
            # Sendet die Summe und den Durchschnitt an den Client
            client_socket.sendall(struct.pack('2i', sum(values), average))
            # Wartet eine Sekunde
            time.sleep(1)
    finally:
        # Schließt die Server-Sockets
        server.close()
        server3.close()

# Funktion für den Berichtprozess
def report_process():
    # Erstellt einen TCP-Client-Socket
    client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Verbindet sich zum Server auf Port 9996
    while True: 
        try:
            client3.connect(('localhost', 9996))
            break
        except ConnectionRefusedError:
            # Falls die Verbindung fehlschlägt, versucht es erneut nach einer Sekunde
            time.sleep(1)
            continue
    
    try:
        while True: #Schleife zum endlosen ausführen des Prozesses
            # Empfängt 8 Bytes vom Server
            data = client3.recv(8)
            # Entpackt die empfangenen Daten (Summe und Durchschnitt)
            sum, avg = struct.unpack('2i', data)
            # Gibt die Summe und den Durchschnitt mit einem Zeitstempel aus
            print(f"| {time.strftime('%H:%M:%S')} | {sum} | {avg} |")
    finally:
        # Schließt den Client-Socket
        client3.close()

