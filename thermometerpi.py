import RPi.GPIO as GPIO
import time
import datetime
import pickle

count = 0
temps = []

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

def SendMessage(address, port, temp, time):
	id = 1
	payload = [id, temp, time]
	payload_pickle = pickle.dumps(payload)
	# send payload_pickle via socket

while True:
	# check for wake up message
	time.sleep(0.5)

while True:
	# read from thermometer and add to temps list
	count += 1
	if count == 5:
		timeRead = datetime.datetime.now()
	elif count == 10:
		tempToSend = sum(temps)/len(temps)
		del temps[:]
		SendMessage(ip_address, server_port, tempToSend, timeRead)
		count = 0;
	time.sleep(1)