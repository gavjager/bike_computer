#!/usr/bin/python3
import socket
import sys

HOST, PORT = "192.168.1.207", 9999

# send command line arguments as a string
data = "hello"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # connect and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    received = str(sock.recv(1024), "utf-8")

print(f"Sent:       {data}")
print(f"Received:   {received}")
