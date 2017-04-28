import sys
import pickle
import json
import socket
import time

sock1_connect = ('172.29.124.24', 8000)
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock2_connect = ('172.29.124.24', 8001)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


print "connection complete"

#Create JSON object from temp1 (float), time1 (string), 
#temp2 (float), and time2 (string) and pickle the object 
def server_pickle(temp1, time1, temp2, time2):
	data = {"id_1":{"time": time1, "temp": temp1}, "id_2":{"time": time2, "temp": temp2}}
	return pickle.dumps(json.dumps(data))

#Unpickles JSON object, and returns contents as a dictionary
def server_unpickle(pickled_data):
    return json.loads(pickle.loads(pickled_data))

def send_data1(obj1):
	try:
		#Connect to socket 1
		sock1.connect(sock1_connect)
		print "Socket 1 connected"
		# Send data
		sock1.sendall(obj1)
		print "Sent data over socket 1"

	finally:
		print 'Closing socket 1'
		sock1.close()
		
def send_data2(obj2):
	try:
		#Connect to socket 2
		sock2.connect(sock2_connect)
		print "Socket 2 connected"
		# Send data
		sock2.sendall(obj2)
		print "Sent data over socket 2"

	finally:
		print 'Closing socket 2'
		sock2.close()

dict1 = {"time": "01:25:00", "temp": 22.1}
dict2 = {"time": "01:25:01", "temp": 22.2}
dict3 = {"time": "01:25:02", "temp": 22.3}
dict4 = {"time": "01:25:03", "temp": 22.4}


try:

		pick_obj1 = server_pickle(dict1["temp"], dict1["time"], dict2["temp"], dict2["time"])
		send_data1(pick_obj1)
		time.sleep(1)
		pick_obj2 = server_pickle(dict3["temp"], dict3["time"], dict4["temp"], dict4["time"])
		send_data2(pick_obj2)
		time.sleep(1)
	
finally:
	print "close"



