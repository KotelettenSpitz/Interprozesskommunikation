import random, time, os
from multiprocessing import shared_memory, Semaphore

ALLOC_SIZE = 64
ALLOC_NAME_1 = "mem1"
ALLOC_NAME_2 = "mem2"

mem_alloc_1 = shared_memory.SharedMemory(ALLOC_NAME_1, True, ALLOC_SIZE)
mem_alloc_2 = shared_memory.SharedMemory(ALLOC_NAME_2, True, ALLOC_SIZE)

print(mem_alloc_1)
print(mem_alloc_1.buf)
print(len(mem_alloc_1.buf))

def random_input():
    return random.randint(0, 10)

while True:
    x = 0
    while True:
        time.sleep(0.1)
        val = random_input()
        mem_alloc_1.buf[x] = val
        mem_alloc_2.buf[x] = val
        x += 1
        #print(val)
        if x == ALLOC_SIZE:
            break

time.sleep(1000)