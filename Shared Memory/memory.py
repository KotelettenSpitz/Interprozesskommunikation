import os, mmap

# Funktion zum Erstellen eines Shared Memory Bereichs
def create_shared_memory(name, size):
    try:
        # Erstellen oder Öffnen einer Datei für den Shared Memory Bereich
        shm_fd = os.open(name, os.O_CREAT | os.O_TRUNC | os.O_RDWR)
        # Festlegen der Größe des Shared Memory Bereichs
        os.ftruncate(shm_fd, size)
        # Erstellen eines mmap-Objekts, das den Shared Memory Bereich repräsentiert
        speicher = mmap.mmap(shm_fd, size, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ)
        os.close(shm_fd)  # Schließen der Datei
        return speicher  # Rückgabe des mmap-Objekts
    except FileNotFoundError:
        print(f"Shared memory '{name}' nicht gefunden.")
        exit(1)  # Beenden des Programms bei Fehler
    except Exception as e:
        print(f"Fehler beim Zugriff auf Shared Memory. '{name}': {e}")
        exit(1)  # Beenden des Programms bei Fehler

# Funktion zum Öffnen eines bestehenden Shared Memory Bereichs
def open_shared_memory(name, size):
    try:
        # Öffnen der Datei für den Shared Memory Bereich
        shm_fd = os.open(name, os.O_RDWR)
        speicher = mmap.mmap(shm_fd, size, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ)
        os.close(shm_fd)
        return speicher
    except FileNotFoundError:
        print(f"Shared memory '{name}' nicht gefunden.")
        exit(1)
    except Exception as e:
        print(f"Fehler beim Zugriff auf Shared Memory. '{name}': {e}")
        exit(1)
