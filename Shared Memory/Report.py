import time, os, mmap, posix_ipc

ALLOC_SIZE = 8
ALLOC_NAME = "/dev/shm/mem3"
SEMAPHORE_NAME = "/semaphore"

try:
    posix_ipc.unlink_semaphore(SEMAPHORE_NAME)
except posix_ipc.ExistentialError:
    pass

semaphore = posix_ipc.Semaphore(SEMAPHORE_NAME, posix_ipc.O_CREAT, initial_value=1)

def open_shared_memory(name, size):
    try:
        shm_fd = os.open(name, os.O_RDWR)
        speicher = mmap.mmap(shm_fd, size, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ)
        os.close(shm_fd)
        return speicher
    except FileNotFoundError:
        print(f"Shared memory '{name}' not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while accessing shared memory '{name}': {e}")
        exit(1)

mem_alloc = open_shared_memory(ALLOC_NAME, ALLOC_SIZE)

spalten = ["Zeit", "Summe", "Mittelwert"]
design = "+" + "+".join(["-" * (len(col) + 2) for col in spalten]) + "+"

print(design)
print("|", end="")
for col in spalten:
    print(f" {col} |", end="")
print("\n" + design)

try:
    x = 0
    while True:
        time.sleep(1)

        semaphore.acquire()
        summe = int.from_bytes(mem_alloc[:8], 'little')
        semaphore.release()

        count = summe

        if count > 0:
            mean = summe / 64
        else:
            mean = 0

        print(f"| {time.strftime('%H:%M:%S')} | {summe:5} | {mean:9.2f} |")

finally:
    semaphore.unlink()
