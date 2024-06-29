import os
import socket
import random
import time
import signal
import sys
import struct

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s

server1 = create_socket()
server2 = create_socket()
client = create_socket()
server = create_socket()
server3 = create_socket()
client3 = create_socket()

def conv_process():
    server1.bind(('localhost', 9999))
    server2.bind(('localhost', 9998))
    
    server1.listen(1)
    server2.listen(1)
    client_socket1, addr = server1.accept()
    client_socket2, addr = server2.accept()

    try:
        while True:
            prevalue = random.randint(1, 100)
            value = struct.pack('i', prevalue)
            client_socket1.sendall(value)
            client_socket2.sendall(value)
            time.sleep(1)
    except KeyboardInterrupt:
        server1.close()
        server2.close()

def log_process():
    while True:
        try:
            client.connect(('localhost', 9999))
            break
        except ConnectionRefusedError:
            time.sleep(1)
            continue
    try:
        while True:
            data = client.recv(4)
            value = struct.unpack('i', data)[0]
            with open("log.txt", "a") as log:
                log.write(str(value) + "\n")
                log.flush()
    except KeyboardInterrupt:
        client.close()

def stat_process():
    while True:
        try:
            server.connect(('localhost', 9998))
            break
        except ConnectionRefusedError:
            time.sleep(1)
            continue

    server3.bind(('localhost', 9996))
    server3.listen(1)
    client_socket, addr = server3.accept()

    values = []
    try:
        while True:
            data = server.recv(4)
            value = struct.unpack('i', data)[0]
            values.append(value)
            average = sum(values) // len(values)
            client_socket.sendall(struct.pack('2i', sum(values), average))
            time.sleep(1)
    except KeyboardInterrupt:
        server.close()
        server3.close()


def report_process():
    while True:
        try:
            client3.connect(('localhost', 9996))
            break
        except ConnectionRefusedError:
            time.sleep(1)
            continue

    try:
        while True:
            data = client3.recv(8)
            sum, avg = struct.unpack('2i', data)
            print(f"| {time.strftime('%H:%M:%S')} | {sum} | {avg} |")
    except KeyboardInterrupt:
        client3.close()
