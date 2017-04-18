import RPi.GPIO as GPIO
import time

while True:
	if GPIO.input(7):
		print('Fire detected!')
		# send message to thermometers and maps via sockets
		break
	time.sleep(0.5)

while True:
	time.sleep(10)
	# get tuple from both thermometers
	# unpickle both objects
	# compile into JSON object
	# store into MongoDB
	# pickle JSON
	# send to map pi via socket