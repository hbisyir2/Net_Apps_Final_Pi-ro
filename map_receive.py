import socket
import json
import pickle
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8100))
sock.listen(3)

conn, addr = sock.accept()
print("Connected at", addr)

while True:
    try:
        data = conn.recv(4096)
    except ConnectionResetError:
        print("Connection to server lost, retrying...")
        conn, addr = sock.accept()
        print("Connected at", addr)
    else:
        if data:
            print("Message received")
            print(data)
            d = json.loads(pickle.loads(data))
            print(d)

    time.sleep(5)
