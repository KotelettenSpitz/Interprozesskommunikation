import time, posix_ipc, struct, os
from memory import open_shared_memory

# Konstanten für Speichergröße, Namen des Shared Memory Bereichs und des Semaphors
ALLOC_SIZE = 16
ALLOC_NAME = "/dev/shm/mem3"
SEMAPHORE_NAME = "/semaphore"

# Versuch, ein eventuell vorhandenes Semaphore zu entfernen
try:
    posix_ipc.unlink_semaphore(SEMAPHORE_NAME)
except posix_ipc.ExistentialError:
    pass  # Falls das Semaphore nicht existiert, einfach weitermachen

# Semaphore wird erstellt
semaphore = posix_ipc.Semaphore(SEMAPHORE_NAME, posix_ipc.O_CREAT, initial_value=1)

# Shared Memory Bereich öffnen
mem_alloc = open_shared_memory(ALLOC_NAME, ALLOC_SIZE)

def report_process():

    # Tabellenüberschrift und Design für die Ausgabe
    spalten = ["Zeit", "Summe", "Mittelwert"]
    design = "+" + "+".join(["-" * (len(col) + 2) for col in spalten]) + "+"

    # Tabellenüberschrift ausgeben
    print(design)
    print("|", end="")
    for col in spalten:
        print(f" {col} |", end="")
    print("\n" + design)
    
    try:
        # Endlosschleife zum Lesen von Werten aus dem Shared Memory Bereich und Ausgabe in tabellarischer Form
        while True:
            semaphore.acquire()  # Semaphore sperren

            # Gesamtsumme aus den ersten 8 Bytes des Shared Memory Bereichs lesen
            total_bytes = int.from_bytes(mem_alloc[:8], 'little')
            # Durchschnitt aus den nächsten 8 Bytes des Shared Memory Bereichs lesen
            avg_bytes = struct.unpack("d", mem_alloc[8:16])[0]

            semaphore.release()  # Semaphore freigeben

            # Aktuelle Zeit, Gesamtsumme und Durchschnitt werden in tabellarischer Form ausgegeben
            print(f"| {time.strftime('%H:%M:%S')} | {total_bytes:5} | {avg_bytes:9.2f} |")
            time.sleep(1)
    finally:
        if os.getpid() == os.getppid():  # Nur der Hauptprozess entfernt das Semaphore
            semaphore.unlink()  # Semaphore entfernen
