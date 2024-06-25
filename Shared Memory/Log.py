import posix_ipc
from memory import open_shared_memory

# Konstanten für Speichergröße, Namen des Shared Memory Bereichs und des Semaphors
ALLOC_SIZE = 64
ALLOC_NAME = "/dev/shm/mem1"
SEMAPHORE_NAME = "/semaphore"

# Versuch, ein eventuell vorhandenes Semaphore zu entfernen
try:
    posix_ipc.unlink_semaphore(SEMAPHORE_NAME)
except posix_ipc.ExistentialError:
    pass  # Falls das Semaphore nicht existiert, einfach weitermachen

# Semaphore wird erstellt
semaphore = posix_ipc.Semaphore(SEMAPHORE_NAME, posix_ipc.O_CREAT, initial_value=1)

# Shared Memory Bereich öffnen
mem_alloc_1 = open_shared_memory(ALLOC_NAME, ALLOC_SIZE)

# Debug
"""
print(f"Shared Memory: {mem_alloc_1}")
print(f"Shared Memory Buffer: {mem_alloc_1[:]}")
print(f"Shared Memory Size: {len(mem_alloc_1)}")
"""

# Erstellen oder Leeren der Logdatei
with open("log.txt", "w") as f:
    pass

# Funktion zum Schreiben von Werten in die Logdatei
def write_to_log(val):
    with open("log.txt", "a") as f:
        f.write(str(val) + "\n")

try:
    # Endlosschleife zum Lesen von Werten aus dem Shared Memory Bereich und Schreiben in die Logdatei
    while True:
        x = 0
        while True:
            semaphore.acquire()  # Semaphore sperren
            val = mem_alloc_1[x]  # Wert aus dem Shared Memory Bereich lesen
            semaphore.release()  # Semaphore freigeben
            write_to_log(val)  # Wert in die Logdatei schreiben
            x += 1
            if x == ALLOC_SIZE:
                break
finally:
    semaphore.unlink()  # Semaphore entfernen
