import socket
import pickle
import select
import json
import RPi.GPIO as GPIO
import time
import sys
import argparse
import threading
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-i1', required=True)
parser.add_argument('-i2', required=True)
parser.add_argument('-i3', required=True)
parser.add_argument('-p1', required=True)
parser.add_argument('-p2', required=True)
parser.add_argument('-p3', required=True)
args = parser.parse_args()

t1_ip = args.i1
t1_port = args.p1
t2_ip = args.i2
t2_port = args.p2
map_ip = args.i3
map_port = args.p3

GPIO.setmode(GPIO.BOARD)

Vin = 7

GPIO.setup(Vin, GPIO.IN)

#while True:
#    if GPIO.input(Vin):
#        print('Fire detected!')
        # send message to thermometers and maps via sockets
#        break
#    time.sleep(1)

sock1_map_connect = (map_ip, int(map_port))
sock1_map = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock1_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock1_temp.bind((t1_ip, int(t1_port)))
sock2_temp.bind((t2_ip, int(t2_port)))

sock1_temp.listen(3)
sock2_temp.listen(3)

sock1_temp.settimeout(5.0)
sock2_temp.settimeout(5.0)

def server_pickle(id, temp, time):
    data = {"id": id, "time": time, "temp": temp}
    return pickle.dumps(json.dumps(data))


def map_pickle(temp_list):
    return pickle.dumps(json.dumps(temp_list), protocol=1, fix_imports=False)


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

def send_every_ten():
    global data_list
    send_data(map_pickle(data_list))
    threading.Timer(10.0, send_every_ten).start()

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
	
data_list = [{'id': 1, 'temp': 0, 'time': 'now'}, {'id': 2, 'temp': 0, 'time': 'now'}]
send_every_ten()
		
while True:
    conn = None
    try:
        ready, _, _ = select.select(socket_list, [], [])

        for sock in ready:
            conn, addr = sock.accept()
            data = conn.recv(256)
            print("Message received")
            d = server_unpickle(data)
            print(d)
            if d['id'] == 1:
                data_list[0] = d
            else:
                data_list[1] = d
    except KeyboardInterrupt:
        print("Server closed by user.")
        if conn:
            conn.close()
        break
    except socket.timeout:
        print("Connection timed out...")
