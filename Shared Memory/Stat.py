import time, posix_ipc, struct
from memory import create_shared_memory
from memory import open_shared_memory

# Konstanten für Speichergrößen, Namen der Shared Memory Bereiche und des Semaphors
ALLOC_SIZE_1 = 64
ALLOC_SIZE_2 = 16
ALLOC_NAME_1 = "/dev/shm/mem2"
ALLOC_NAME_2 = "/dev/shm/mem3"
SEMAPHORE_NAME = "/semaphore"

# Versuch, ein eventuell vorhandenes Semaphore zu entfernen
try:
    posix_ipc.unlink_semaphore(SEMAPHORE_NAME)
except posix_ipc.ExistentialError:
    pass  # Falls das Semaphore nicht existiert, einfach weitermachen

# Semaphore wird erstellt
semaphore = posix_ipc.Semaphore(SEMAPHORE_NAME, posix_ipc.O_CREAT, initial_value=1)

# Shared Memory Bereiche öffnen bzw. erstellen
mem_alloc_1 = open_shared_memory(ALLOC_NAME_1, ALLOC_SIZE_1)
mem_alloc_2 = create_shared_memory(ALLOC_NAME_2, ALLOC_SIZE_2)

total = 0
y = 1

try:
    # Endlosschleife zum Lesen von Werten aus dem 1. Shared Memory Bereich und Schreiben von Ergebnissen in den 2.
    while True:
        summe = 0
        x = 0
        while True:
            semaphore.acquire()  # Semaphore sperren
            summe = mem_alloc_1[x]  # Wert aus dem ersten Shared Memory Bereich lesen
            semaphore.release()  # Semaphore freigeben
            total += summe  # Summe der gelesenen Werte zur Gesamtsumme hinzufügen
            x += 1
            if x == ALLOC_SIZE_1:  # Wenn das Ende des Speicherbereichs erreicht ist, Schleife beenden
                avg = total / (y * 64)
                total_byte = total.to_bytes(8, 'little')  # Gesamtsumme in Byte array
                avg_byte = bytearray(struct.pack("d", avg))  # Durchschnitt in Byte array
                result_bytes = bytearray(total_byte)  # Ergebnis in Byte-Array umwandeln
                result_bytes.extend(avg_byte)  # Durchschnitts-Byte-Array an result_bytes anhängen
                semaphore.acquire()
                mem_alloc_2[:8] = total_byte  # Gesamtsumme in den zweiten Shared Memory Bereich schreiben (1-8 Bytes)
                mem_alloc_2[8:16] = avg_byte  # Durchschnitt in den zweiten Shared Memory Bereich schreiben (9-16 Bytes)
                semaphore.release()
                break
        y += 1  # Zähler für die Anzahl der Durchläufe erhöhen
        time.sleep(1)
finally:
    semaphore.unlink()  # Semaphore entfernen
