import time, posix_ipc, struct
from memory import create_shared_memory
from memory import open_shared_memory

ALLOC_SIZE_1 = 64
ALLOC_SIZE_2 = 16
ALLOC_NAME_1 = "/dev/shm/mem2"
ALLOC_NAME_2 = "/dev/shm/mem3"
SEMAPHORE_NAME = "/semaphore"

try:
    posix_ipc.unlink_semaphore(SEMAPHORE_NAME)
except posix_ipc.ExistentialError:
    pass

semaphore = posix_ipc.Semaphore(SEMAPHORE_NAME, posix_ipc.O_CREAT, initial_value=1)


mem_alloc_1 = open_shared_memory(ALLOC_NAME_1, ALLOC_SIZE_1)
mem_alloc_2 = create_shared_memory(ALLOC_NAME_2, ALLOC_SIZE_2)

total = 0
y = 1

while True:
    summe = 0
    lauf = 0
    x = 0
    while True:
        semaphore.acquire()
        summe = mem_alloc_1[x]
        semaphore.release()
        total += summe
        lauf += summe
        x += 1
        if x == ALLOC_SIZE_1:
            avg = total / (y * 64)
            total_byte = total.to_bytes(8, 'little')
            avg_byte = bytearray(struct.pack("d", avg))
            result_bytes = bytearray(total_byte)
            result_bytes.extend(avg_byte)
            semaphore.acquire()
            mem_alloc_2[:8] = total_byte
            mem_alloc_2[8:16] = avg_byte
            semaphore.release()
            break
    y += 1

    time.sleep(1)

time.sleep(1000)
semaphore.unlink()