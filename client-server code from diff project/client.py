import sys
import pickle
import json
import socket
import time
import select
import argparse
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from datetime import datetime

#Hardware SPI config
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Parse arguments, requires IP address of Raspberry Pi,
#and zipcode it is running in
parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True)
args = parser.parse_args()
ip_address = args.i

#Create TCP connection to listen on#####################################
try:

	listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listen_sock.bind(('', 8001))
	listen_sock.listen(3)
	socket_list = (listen_sock,)
	
except Exception:
	print("Error connecting sockets: ", Exception)
	send_sock.close()
	listen_sock.close()
	sys.exit(1)
########################################################################


#Create JSON object from time and power and pickle the object 
def data_pickle(time, power):
	data = {"time": time, "power": power}
	return pickle.dumps(json.dumps(data))


#Unpickles JSON object, and returns contents as a dictionary
def data_unpickle(pickled_data):
    return json.loads(pickle.loads(pickled_data))


#Send data over socket
def send_data(obj1):
	try:
		# Send data
		send_sock.sendall(obj1)
		print("Sent data to server \n")

	except Exception:
		print("Error sending data over TCP socket: ", Exception)
		send_sock.close()
		listen_sock.close()
		sys.exit(1)
        
#SPI read data
def read_spi():
    value = mcp.read_adc_difference(0)
    return value*3.3/1023.0


try:
	cont = True
	while cont:
		power = read_spi()
		t = datetime.now().strftime("%I:%M%p")
		send_connect = (ip_address, 8000) #Socket for sending data
		send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		send_sock.connect(send_connect)	
		send_data(data_pickle(t, power))
		send_sock.close()

		ready, _, _ = select.select(socket_list, [], [])

		for sock in ready:
			conn, addr = sock.accept()
			data = conn.recv(256)
			print("Message received")
		
		unpick = data_unpickle(data)
		print("Sun Altitude: %s,  Sun Angle: %s" % (unpick["altitude"], unpick["angle"]))
		print()
		
		time.sleep(10)
		
	
finally:
	print("Closing all connections")
	send_sock.close()
	listen_sock.close()



