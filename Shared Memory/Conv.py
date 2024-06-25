import random, posix_ipc
from memory import create_shared_memory

ALLOC_SIZE = 64
ALLOC_NAME_1 = "/dev/shm/mem1"
ALLOC_NAME_2 = "/dev/shm/mem2"
SEMAPHORE_NAME = "/semaphore"

try:
    posix_ipc.unlink_semaphore(SEMAPHORE_NAME)
except posix_ipc.ExistentialError:
    pass

semaphore = posix_ipc.Semaphore(SEMAPHORE_NAME, posix_ipc.O_CREAT, initial_value=1)


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
            val = random.randint(0, 99)
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