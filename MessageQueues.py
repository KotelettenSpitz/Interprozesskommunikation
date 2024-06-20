import time
import random
import posix_ipc
import struct

def conv_process():
    while True:
        value = random.randint(0, 1023)
        if value <= 1023 and value >= 0:
            SendToQueue("/mq1", value, None)
            SendToQueue("/mq2", value, None)
        time.sleep(1)

def log_process():
    with open('log.txt', 'a') as log:
        while True:
            value = ReceiveFromQueue("/mq1")
            log.write(f"{value}\n")
            log.flush()

def stat_process():
    sum_values = 0
    count = 0
    while True:
        value = ReceiveFromQueue("/mq2")
        if value is not None:
            sum_values += value
            count += 1
            average = sum_values / count
            SendToQueue("/mq3", sum_values, average)
        time.sleep(1)

def report_process():
    while True:
        sum_values, average = ReceiveFromQueue("/mq3")
        if sum_values is not None and average is not None:
            print(f"Summe: {sum_values}, Durchschnitt: {average}")
        time.sleep(1)

def CreateQueue():
    try:
        posix_ipc.MessageQueue("/mq1", flags=posix_ipc.O_CREAT, mode=0o600, max_messages=10, max_message_size=1024)
        posix_ipc.MessageQueue("/mq2", flags=posix_ipc.O_CREAT, mode=0o600, max_messages=10, max_message_size=1024)
        posix_ipc.MessageQueue("/mq3", flags=posix_ipc.O_CREAT, mode=0o600, max_messages=10, max_message_size=1024)
    except posix_ipc.ExistentialError:
        pass

def SendToQueue(name, value, value2):
    mq = posix_ipc.MessageQueue(name)
    if name == "/mq1" or name == "/mq2":
        mq.send(struct.pack('i', value), 0)
    elif name == "/mq3":
        mq.send(struct.pack('2i', value, int(value2)), 0)

def ReceiveFromQueue(name):
    mq = posix_ipc.MessageQueue(name)
    if name == "/mq1" or name == "/mq2":
        prevalue, _ = mq.receive()
        value = struct.unpack('i', prevalue)[0]
        return value
    elif name == "/mq3":
        try:
            message, _ = mq.receive(timeout=1)
            sum_values, average = struct.unpack('2i', message)
            return sum_values, average
        except posix_ipc.BusyError:
            return None, None

def DeleteQueue(name):
    try:
        mq = posix_ipc.MessageQueue(name)
        mq.unlink()
    except posix_ipc.ExistentialError:
        pass