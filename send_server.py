import sys
import pickle
import json
import socket

sock1_connect = ('10.0.0.78', 8000)
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock2_connect = ('10.0.0.78', 8001)
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
    

send1 = "Hello Jason"
send2 = "More data"

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


send_data2(send2)
send_data1(send1)

