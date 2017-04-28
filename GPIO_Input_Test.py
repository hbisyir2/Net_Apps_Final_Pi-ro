import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.IN)

while True:
	print('Waiting for fire...')
	if GPIO.input(7):
		print('Fire detected!')
		# send message to thermometers and maps via sockets
		#GPIO.cleanup()
		break
	time.sleep(0.5)