import socket
import pickle
import select
import json
import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)

Vin = 7

GPIO.setup(Vin, GPIO.IN)

#while True:
#    if GPIO.input(Vin):
#        print('Fire detected!')
        # send message to thermometers and maps via sockets
#        break
#    time.sleep(1)

MAP1_ADDRESS = "localhost"

sock1_map_connect = (MAP1_ADDRESS, 8100)
sock1_map = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock1_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock1_temp.settimeout(5.0)
sock2_temp.settimeout(5.0)

sock1_temp.bind(('', 8000))
sock2_temp.bind(('', 8001))

sock1_temp.listen(3)
sock2_temp.listen(3)


def server_pickle(id, temp, time):
    data = {"id": id, "time": time, "temp": temp}
    return pickle.dumps(json.dumps(data))


def map_pickle(temp_list):
    return pickle.dumps(json.dumps(temp_list))


def server_unpickle(pickled_data):
    return json.loads(pickle.loads(pickled_data))


def send_data(obj1):
    try:
        print("Sending data to map... ", end="")
        sock1_map.sendall(obj1)
        print("sent.")

    except socket.gaierror:
        print("\nAddress", MAP1_ADDRESS, "could not be found")
    except ConnectionResetError:
        print("\nError: existing connection was closed.")


socket_list = (sock1_temp, sock2_temp)

while True:
    try:
        print("Connecting to map... ", end="")
        sock1_map.connect(sock1_map_connect)
        print("connected.")
        break
    except ConnectionRefusedError:
        print("\nConnection refused, is client listening?")
        sleep = 5
        print("Retry in", sleep, "seconds")
        time.sleep(sleep)

while True:
    conn = None
    try:
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
            sock.close()

        # send data_list to mappi
        send_data(map_pickle(data_list))
    except KeyboardInterrupt:
        print("Server closed by user.")
        if conn:
            conn.close()
        break
