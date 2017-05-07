import os
import glob
import time
import datetime
import pickle
import argparse
import socket

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

count = 0
temps = []

# send payload_pickle via socket
def PickleObject(temp, time):
	id = 1
	payload = {'id':id, 'temp':temp, 'time':time}
	payload_pickle = pickle.dumps(payload)
	return payload_pickle
	
def SendMessage(address, port, temp, time):
	try:
		sentPickle = PickleObject(temp, time)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((address, port))
		s.send(sentPickle)
	except Exception:
		print("Error sending message: " Exception)
	finally:
		s.close()

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c, temp_f
		
# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True)
parser.add_argument('-p', required=True)
args = parser.parse_args()

ip_address = args.i
port = args.p

while True:
	temp_c, temp_f = read_temp()
	if temp_f == 0:
		break
	else:
		temps.append(temp_f)
		count += 1
		if count == 5:
			timeRead = datetime.datetime.now()
			timeReadStr = timeRead.strftime('%Y/%m/%d %H:%M:%S')
		elif count == 10:
			tempToSend = sum(temps)/len(temps)
			print(timeReadStr)
			print(tempToSend)
			del temps[:]
			SendMessage(ip_address, port, tempToSend, timeReadStr)
			count = 0
		time.sleep(0.5)
