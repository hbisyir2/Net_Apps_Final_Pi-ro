import datetime
import time
from Adafruit_LED_Backpack import SevenSegment
import RPi.GPIO as GPIO
import argparse
import socket
import json
import pickle
import threading

LED1_red = 16
LED1_green = 18
LED2_red = 21
LED2_green = 23

Vin = 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(Vin, GPIO.IN)

GPIO.setup(LED1_green, GPIO.OUT)
GPIO.setup(LED1_red, GPIO.OUT)
GPIO.setup(LED2_green, GPIO.OUT)
GPIO.setup(LED2_red, GPIO.OUT)

GPIO.output(LED1_green, GPIO.LOW)
GPIO.output(LED1_red, GPIO.LOW)
GPIO.output(LED2_green, GPIO.LOW)
GPIO.output(LED2_red, GPIO.LOW)

disp1 = SevenSegment.SevenSegment(address=0x70)
disp2 = SevenSegment.SevenSegment(address=0x74)

disp1.begin()
disp2.begin()
disp1.clear()
disp2.clear()
disp1.write_display()
disp2.write_display()

parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True)
parser.add_argument('-p', required=True)
args = parser.parse_args()

ip_address = args.i
port = args.p

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip_address, int(port)))
sock.listen(3)

rightNow = datetime.datetime.now()
rightNow = rightNow.strftime('%Y/%m/%d %H:%M:%S')

LED1_dict = {'id': 1, 'temp': 0, 'time': rightNow}
LED2_dict = {'id': 2, 'temp': 0, 'time': rightNow}

def UpdateDisplay(display, timeTaken):

    if timeTaken == 'now':
        display.clear()
        display.write_display()
        return
    timeTaken = datetime.datetime.strptime(timeTaken, '%Y/%m/%d %H:%M:%S')
    timeNow = datetime.datetime.now()
    timeDiff = timeNow - timeTaken
    minutesDiff = timeDiff.seconds//60
    secondsDiff = timeDiff.seconds%60

    display.clear()
    display.set_colon(1)
    displaym10 = minutesDiff//10
    if displaym10 >= 10:
        displaym10 = 9
    displaym1 = minutesDiff%10
    if displaym1 >= 10:
        displaym1 = 9
    displays10 = secondsDiff//10
    if displays10 >= 10:
        displays10 = 9
    displays1 = secondsDiff%10
    if displays1 >= 10:
        displays1 = 9

    if displaym10 > 0:
        display.set_digit(0, displaym10)
    if displaym1 > 0 or displaym10 > 0:
        display.set_digit(1, displaym1)
    display.set_digit(2, displays10)
    display.set_digit(3, displays1)
    display.write_display()

def UpdateLED(LED_g, LED_r, temp):
    if temp == 0:
        GPIO.output(LED_r, GPIO.LOW)
        GPIO.output(LED_g, GPIO.LOW)
        return
    lowThresh = 80
    highThresh = 90
    if temp <= lowThresh:
        GPIO.output(LED_r, GPIO.LOW)
        GPIO.output(LED_g, GPIO.HIGH)
    elif temp <= highThresh:
        GPIO.output(LED_r, GPIO.HIGH)
        GPIO.output(LED_g, GPIO.HIGH)
    else:
        GPIO.output(LED_r, GPIO.HIGH)
        GPIO.output(LED_g, GPIO.LOW)

def UpdateTime():
    global LED1_dict, LED2_dict, disp1, disp2
    threading.Timer(1.0, UpdateTime).start()
    UpdateDisplay(disp1, LED1_dict['time'])
    UpdateDisplay(disp2, LED2_dict['time'])
    print('Updating time on displays\n')

UpdateTime()

#while True:
#    print('Waiting for fire...')
#    if GPIO.input(7):
#        print('Fire detected!')
#        break
#    time.sleep(0.5)

while True:
    conn, addr = sock.accept()
    print("Connected to server at", addr)
    try:
        data = conn.recv(4096)
    except ConnectionResetError:
        print("Connection to server lost, retrying...")
        conn, addr = sock.accept()
        print("Connected at", addr)
    else:
        if data:
            print("Message received")
            d = json.loads(pickle.loads(data))
            # d is a list of dictionaries, each dictionary containing a time, id, and temp. Ex:
            # [{'time': '2017-05-05 15:29:43.658152', 'id': 1, 'temp': 22.1}, {'time': '2017-05-05 15:29:40.686621', 'id': 2, 'temp': 22.2}]
            if len(d) == 1:
                if d[0]['id'] == 1:
                    LED1_dict = d[0]
                elif d[0]['id'] == 2:
                    LED2_dict = d[0]
            else:
                if d[0]['id'] == 1:
                    LED1_dict = d[0]
                    LED2_dict = d[1]
                elif d[0]['id'] == 2:
                    LED1_dict = d[1]
                    LED2_dict = d[0]
			#UpdateDisplay(disp1, LED1_dict['time'])
			#UpdateDisplay(disp2, LED2_dict['time'])
            UpdateLED(LED1_green, LED1_red, LED1_dict['temp'])
            UpdateLED(LED2_green, LED2_red, LED2_dict['temp'])

    #time.sleep(10)