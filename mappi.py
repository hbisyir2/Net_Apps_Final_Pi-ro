import datetime
import time
from Adafruit_LED_Backpack import SevenSegment
import RPi.GPIO as GPIO

LED1_red = 
LED1_green = 
LED2_red = 
LED2_green = 

GPIO.setup(LED1_green, GPIO.OUT)
GPIO.setup(LED1_red, GPIO.OUT)
GPIO.setup(LED2_green, GPIO.OUT)
GPIO.setup(LED2_red, GPIO.OUT)

GPIO.output(LED1_green, GPIO.LOW)
GPIO.output(LED1_red, GPIO.LOW)
GPIO.output(LED2_green, GPIO.LOW)
GPIO.output(LED2_red, GPIO.LOW)

disp1 = SevenSegment.SevenSegment(address=0x70)
disp2 = SevenSegment.SevenSegment(address=0x77)

disp1.begin()
disp2.begin()
disp1.set_colon(1)
disp2.set_colon(1)

def UpdateDisplay(display, timeTaken):
	timeNow = datetime.datetime.now()
	timeDiff = timeNow - timeTaken
	minutesDiff = timeDiff.seconds//60
	secondsDiff = timeDiff.seconds%60
	
	display.clear()
	displaym10 = minutesDiff//10
	if displaym10 >= 10:
		displaym10 = 9
	displaym1 = minutesDiff%10:
	if displaym1 >= 10:
		displaym1 = 9
	displays10 = secondsDiff//10
	if displays10 >= 10:
		displays10 = 9
	displays1 = secondsDiff%10
	if displays1 >= 10:
		displays1 = 9
	display.set_digit(0, displaym10)
	display.set_digit(1, displaym1)
	display.set_digit(2, displays10)
	display.set_digit(3, displays1)
	display.write_display()
	
def UpdateLED(LED_g, LED_r, temp):
	lowThresh = 70
	highThresh = 80
	if temp <= lowThresh:
		GPIO.output(LED_r, GPIO.LOW)
		GPIO.output(LED_g, GPIO.HIGH)
	elif temp <= highThresh:
		GPIO.output(LED_r, GPIO.HIGH)
		GPIO.output(LED_g, GPIO.HIGH)
	else
		GPIO.output(LED_r, GPIO.HIGH)
		GPIO.output(LED_g, GPIO.LOW)
		
while True:
	# wait for wake up message
	time.sleep(0.5)
		
while True:
	time.sleep(10)
	# get JSON from server
	# unpickle object
	# seperate into variables
	# call functions to update hardware