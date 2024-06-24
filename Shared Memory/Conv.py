import random, os, mmap, posix_ipc

ALLOC_SIZE = 64
ALLOC_NAME_1 = "/dev/shm/mem1"
ALLOC_NAME_2 = "/dev/shm/mem2"
SEMAPHORE_NAME = "/semaphore"

try:
    posix_ipc.unlink_semaphore(SEMAPHORE_NAME)
except posix_ipc.ExistentialError:
    pass

semaphore = posix_ipc.Semaphore(SEMAPHORE_NAME, posix_ipc.O_CREAT, initial_value=1)

def create_shared_memory(name, size):
    shm_fd = os.open(name, os.O_CREAT | os.O_TRUNC | os.O_RDWR)
    os.ftruncate(shm_fd, size)
    speicher = mmap.mmap(shm_fd, size, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ)
    os.close(shm_fd)
    return speicher

mem_alloc_1 = create_shared_memory(ALLOC_NAME_1, ALLOC_SIZE)
mem_alloc_2 = create_shared_memory(ALLOC_NAME_2, ALLOC_SIZE)

"""
print(f"Shared Memory 1: {mem_alloc_1}")
print(f"Shared Memory 1 Buffer: {mem_alloc_1[:]}")
print(f"Shared Memory 1 Size: {len(mem_alloc_1)}")

print(f"Shared Memory 2: {mem_alloc_2}")
print(f"Shared Memory 2 Buffer: {mem_alloc_2[:]}")
print(f"Shared Memory 2 Size: {len(mem_alloc_2)}")
"""

try:
    while True:
        x = 0
        while True:
            val = random.randint(1, 99)
            semaphore.acquire()
            mem_alloc_1[x] = val
            mem_alloc_2[x] = val
            semaphore.release()
            x += 1
            if x == ALLOC_SIZE:
                break

    time.sleep(1000)
finally:
    sem.unlink()