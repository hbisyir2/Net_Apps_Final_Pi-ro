import collections
import argparse
import datetime
import requests
import time
import json
import sys
import math
import ephem
import socket
import pickle
import select

#Parse arguments, requires IP address of Raspberry Pi,
#and zipcode it is running in
parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True)
parser.add_argument('-z', required=True)
args = parser.parse_args()
ip_address = args.i
zipcode = args.z


#Get weather data ######################################################
url = 'http://api.openweathermap.org/data/2.5/forecast/daily?zip=' + str(zipcode) + ',us&cnt=16&APPID=00d0fe518cb4d72c67a854cca7963815'
response = requests.get(url)

try:
	if(response.ok):
		str_response = response.content.decode('utf-8')
		weatherdata = json.loads(str_response)
		latitude = weatherdata['city']['coord']['lat']
		longitude = weatherdata['city']['coord']['lon']

		print ("Latitude: ", latitude, " Longitude: ", longitude, '\n')

		weatherDict = {}
		x=0;
		for keys in weatherdata['list']:
			date = weatherdata['list'][x]['dt']
			weatherCond = weatherdata['list'][x]['weather'][0]['main']
			print("Day ", x, " : ", str(weatherCond))
			if(weatherdata['list'][x]['clouds'] < 20):
				weatherDict[date] = True
			else:
				weatherDict[date] = False
			x+=1
	else:
		response.raise_for_status()
	
	weatherDict_o = collections.OrderedDict(sorted(weatherDict.items()))

except Exception:
	print("Weather API Error: ", Exception)
########################################################################

#Create JSON object from sun angle and altitude and pickle the object 
def data_pickle(altitude, angle):
	data = {"altitude": altitude, "angle": angle}
	return pickle.dumps(json.dumps(data))

#Un pickles and JSONs an object
def data_unpickle(pickled_data):
    return json.loads(pickle.loads(pickled_data))

#Send data over socket
def send_data(obj1):
	try:
		# Send data
		send_sock.sendall(obj1)
		print("Sent data to RPi")

	except Exception:
		print("Error sending data over TCP socket: ", Exception)
		send_sock.close()
		listen_sock.close()
		sys.exit(1)

#Create Observer and Sun object using pyephem###########################
panel = ephem.Observer()
panel.lon, panel.lat = longitude, latitude #Lon and Lat gotten from zip above
sun = ephem.Sun()
########################################################################

#Compare sun to current location
#return suns' altitude above horizon and angle to user
def compSun():
	sun.compute(panel)
	return (sun.alt, sun.az)


#Establish TCP connections, begin sending and receiving data############
listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	listen_sock.bind(('', 8000)) #Bind to port 8000
	listen_sock.listen(3)
	socket_list = (listen_sock,)
	
	cont = True
	
	while cont:
		
		ready, _, _ = select.select(socket_list, [], [])

		for sock in ready:
			conn, addr = sock.accept()
			data = conn.recv(256)
			print("Message received")

		print(data_unpickle(data))
		
		sun_loc = compSun()
		print("Sun altitude: %s, Sun Angle: %s" % (ephem.degrees(sun_loc[0]), ephem.degrees(sun_loc[1])))
		print()
		
		time.sleep(1)
		send_connect = (ip_address, 8001)#Socket for sending data
		send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		send_sock.connect(send_connect)	
		send_data(data_pickle(sun_loc[0], sun_loc[1]))
		send_sock.close()

finally:
	listen_sock.close()
	send_sock.close()
########################################################################


















