import time, os, mmap, posix_ipc, struct

ALLOC_SIZE = 16
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
        print(f"Error accessing shared memory '{name}': {e}")
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
    while True:
        semaphore.acquire()

        total_bytes = int.from_bytes(mem_alloc[:8], 'little')
        avg_bytes = struct.unpack("d", mem_alloc[8:16])[0]

        semaphore.release()

        print(f"| {time.strftime('%H:%M:%S')} | {total_bytes:5} | {avg_bytes:9.2f} |")
        time.sleep(1)

finally:
    semaphore.unlink()