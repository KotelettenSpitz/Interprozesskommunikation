import os, mmap, posix_ipc

ALLOC_SIZE_1 = 64
ALLOC_SIZE_2 = 8
ALLOC_NAME_1 = "/dev/shm/mem2"
ALLOC_NAME_2 = "/dev/shm/mem3"
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

def create_shared_memory(name, size):
    try:
        shm_fd = os.open(name, os.O_CREAT | os.O_TRUNC | os.O_RDWR)
        os.ftruncate(shm_fd, size)
        speicher = mmap.mmap(shm_fd, size, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ)
        os.close(shm_fd)
        return speicher
    except FileNotFoundError:
        print(f"Shared memory '{name}' not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while accessing shared memory '{name}': {e}")
        exit(1)

mem_alloc_1 = open_shared_memory(ALLOC_NAME_1, ALLOC_SIZE_1)
mem_alloc_2 = create_shared_memory(ALLOC_NAME_2, ALLOC_SIZE_2)

"""
print(f"Shared Memory 1: {mem_alloc_1}")
print(f"Shared Memory 1 Buffer: {mem_alloc_1[:]}")
print(f"Shared Memory 1 Size: {len(mem_alloc_1)}")
"""

while True:
    total_sum = 0
    x = 0
    while True:
        semaphore.acquire()
        val = mem_alloc_1[x]
        semaphore.release()
        total_sum += val
        x += 1
        if x == ALLOC_SIZE_1:
            break

    data = total_sum.to_bytes(8, 'little')
    semaphore.acquire()
    mem_alloc_2[:8] = data
    semaphore.release()

time.sleep(1000)
sem.unlink()
