import time
import random
import posix_ipc
import struct

def conv_process():
    mq1 = posix_ipc.MessageQueue("/mq1", flags=posix_ipc.O_CREAT, mode=0o600, max_messages=10, max_message_size=1024)
    mq2 = posix_ipc.MessageQueue("/mq2", flags=posix_ipc.O_CREAT, mode=0o600, max_messages=10, max_message_size=1024)
    try:
        while True:
            value = random.randint(0, 1023)
            if value <= 1023 and value >= 0:
                SendToQueue("/mq1", value, None)
                SendToQueue("/mq2", value, None)
            time.sleep(1)
    except KeyboardInterrupt:
        mq1.unlink()
        mq2.unlink()

def log_process():
    with open('log.txt', 'a') as log:
        try:
            while True:
                value = ReceiveFromQueue("/mq1")
                log.write(f"{value}\n")
                log.flush()
        except KeyboardInterrupt:
            pass

def stat_process():
    mq3 = posix_ipc.MessageQueue("/mq3", flags=posix_ipc.O_CREAT, mode=0o600, max_messages=10, max_message_size=1024)
    sum_values = 0
    count = 0
    try:
        while True:
            value = ReceiveFromQueue("/mq2")
            if value is not None:
                sum_values += value
                count += 1
                average = sum_values / count
                SendToQueue("/mq3", sum_values, average)
                time.sleep(1)
    except KeyboardInterrupt:
        mq3.unlink()

def report_process():
    try:
        while True:
            sum_values, average = ReceiveFromQueue("/mq3")
            if sum_values is not None and average is not None:
                print(f"Summe: {sum_values}, Durchschnitt: {average}")
            time.sleep(1)
    except KeyboardInterrupt:
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
        message, _ = mq.receive(timeout=1)
        sum_values, average = struct.unpack('2i', message)
        return sum_values, average