import os, mmap
def create_shared_memory(name, size):
    try:
        shm_fd = os.open(name, os.O_CREAT | os.O_TRUNC | os.O_RDWR)
        os.ftruncate(shm_fd, size)
        speicher = mmap.mmap(shm_fd, size, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ)
        os.close(shm_fd)
        return speicher
    except FileNotFoundError:
        print(f"Shared memory '{name}' nicht gefunden.")
        exit(1)
    except Exception as e:
        print(f"Fehler beim Zugriff auf Shared Memory. '{name}': {e}")
        exit(1)


def open_shared_memory(name, size):
    try:
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
