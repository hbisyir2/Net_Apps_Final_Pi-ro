import sys
import pickle
import json
import socket
import datetime
import time

sock1_connect = ('localhost', 8000)
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock2_connect = ('localhost', 8001)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("connection complete")


# Create JSON object from temp1 (float), time1 (string),
# temp2 (float), and time2 (string) and pickle the object
def server_pickle(id, time, temp):
    data = {"id": id, "time": time, "temp": temp}
    return pickle.dumps(json.dumps(data))


# Unpickles JSON object, and returns contents as a dictionary
def server_unpickle(pickled_data):
    return json.loads(pickle.loads(pickled_data))


def send_data1(obj1):
    try:
        # Connect to socket 1
        sock1.connect(sock1_connect)
        print("Socket 1 connected")
        # Send data
        sock1.sendall(obj1)
        print("Sent data over socket 1")

    finally:
        print('Closing socket 1')
        sock1.close()


def send_data2(obj2):
    try:
        # Connect to socket 2
        sock2.connect(sock2_connect)
        print("Socket 2 connected")
        # Send data
        sock2.sendall(obj2)
        print("Sent data over socket 2")

    finally:
        print('Closing socket 2')
        sock2.close()


dict1 = {"id": 1, "time": str(datetime.datetime.now()), "temp": 22.1}
dict2 = {"id": 2, "time": str(datetime.datetime.now()), "temp": 22.2}

try:
    pick_obj1 = server_pickle(dict1["id"], dict1["time"], dict1["temp"])
    send_data1(pick_obj1)
    time.sleep(1)
    pick_obj2 = server_pickle(dict2["id"], dict2["time"], dict2["temp"])
    send_data2(pick_obj2)
    time.sleep(1)

finally:
    print("close")
