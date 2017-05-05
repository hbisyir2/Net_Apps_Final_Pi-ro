import socket
import pickle
import select
import json
# import RPi.GPIO as GPIO
import time

# while True:
#     if GPIO.input(7):
#         print('Fire detected!')
#         # send message to thermometers and maps via sockets
#         break
#     time.sleep(1)

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock1.bind(('', 8000))
sock2.bind(('', 8001))

sock1.listen(3)
sock2.listen(3)


def server_pickle(id, temp, time):
    data = {"id": id, "time": time, "temp": temp}
    return pickle.dumps(json.dumps(data))


def server_unpickle(pickled_data):
    return json.loads(pickle.loads(pickled_data))

socket_list = (sock1, sock2)

while True:
    time.sleep(5)
    data_list = []

    ready, _, _ = select.select(socket_list, [], [])

    for sock in ready:
        conn, addr = sock.accept()
        data = conn.recv(256)
        print("Message received")
        d = server_unpickle(data)
        print(d)
        data_list.append(d.copy())

    # send data_list to mappi
    print(data_list)

conn.close()
sock.close()
