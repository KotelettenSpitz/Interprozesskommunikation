import random, posix_ipc
from memory import create_shared_memory

# Konstanten für Speichergröße und Namen der Shared Memory Bereiche und des Semaphors
ALLOC_SIZE = 64
ALLOC_NAME_1 = "/dev/shm/mem1"
ALLOC_NAME_2 = "/dev/shm/mem2"
SEMAPHORE_NAME = "/semaphore"

# Versuch, ein eventuell vorhandenes Semaphore zu entfernen
try:
    posix_ipc.unlink_semaphore(SEMAPHORE_NAME)
except posix_ipc.ExistentialError:
    pass  # Falls das Semaphore nicht existiert, einfach weitermachen

# Semaphore wird erstellt
semaphore = posix_ipc.Semaphore(SEMAPHORE_NAME, posix_ipc.O_CREAT, initial_value=1)

# Shared Memory Bereiche erstellen
mem_alloc_1 = create_shared_memory(ALLOC_NAME_1, ALLOC_SIZE)
mem_alloc_2 = create_shared_memory(ALLOC_NAME_2, ALLOC_SIZE)

# Debug
"""
print(f"Shared Memory 1: {mem_alloc_1}")
print(f"Shared Memory 1 Buffer: {mem_alloc_1[:]}")
print(f"Shared Memory 1 Size: {len(mem_alloc_1)}")

print(f"Shared Memory 2: {mem_alloc_2}")
print(f"Shared Memory 2 Buffer: {mem_alloc_2[:]}")
print(f"Shared Memory 2 Size: {len(mem_alloc_2)}")
"""

try:
    # Endlosschleife zum Schreiben von Zufallswerten in die Shared Memory Bereiche
    while True:
        x = 0
        while True:
            val = random.randint(0, 99)
            semaphore.acquire()  # Semaphore sperren
            mem_alloc_1[x] = val  # Wert in den ersten Shared Memory Bereich schreiben
            mem_alloc_2[x] = val
            semaphore.release()  # Semaphore freigeben
            x += 1
            if x == ALLOC_SIZE:
                break
finally:
    semaphore.unlink()  # Semaphore entfernen
