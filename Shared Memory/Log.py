import random, time, os
from multiprocessing import shared_memory, Semaphore

ALLOC_SIZE = 64
ALLOC_NAME = "mem1"

mem_alloc_1 = shared_memory.SharedMemory(ALLOC_NAME, False, ALLOC_SIZE)

print(mem_alloc_1)
print(mem_alloc_1.buf)
print(len(mem_alloc_1.buf))

with open("log.txt", "w") as f:
    pass
def write_to_log(val):
    f = open("log.txt", "a")
    f.write(str(val) + "\n")
    f.close()

while True:
    x = 0
    while True:
        time.sleep(0.1)
        val = mem_alloc_1.buf[x]
        write_to_log(val)
        #print(val)
        x += 1
        if x == ALLOC_SIZE:
            break

time.sleep(1000)