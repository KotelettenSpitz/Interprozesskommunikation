import posix_ipc
from memory import open_shared_memory

ALLOC_SIZE = 64
ALLOC_NAME = "/dev/shm/mem1"
SEMAPHORE_NAME = "/semaphore"

try:
    posix_ipc.unlink_semaphore(SEMAPHORE_NAME)
except posix_ipc.ExistentialError:
    pass

semaphore = posix_ipc.Semaphore(SEMAPHORE_NAME, posix_ipc.O_CREAT, initial_value=1)


mem_alloc_1 = open_shared_memory(ALLOC_NAME, ALLOC_SIZE)

"""
print(f"Shared Memory: {mem_alloc_1}")
print(f"Shared Memory Buffer: {mem_alloc_1[:]}")
print(f"Shared Memory Size: {len(mem_alloc_1)}")
"""

with open("log.txt", "w") as f:
    pass


def write_to_log(val):
    with open("log.txt", "a") as f:
        f.write(str(val) + "\n")


try:
    while True:
        x = 0
        while True:
            semaphore.acquire()
            val = mem_alloc_1[x]
            semaphore.release()
            write_to_log(val)
            x += 1
            if x == ALLOC_SIZE:
                break

    time.sleep(1000)
finally:
    sem.unlink()