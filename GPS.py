#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import serial
import time
import csv

## Threads for blinking LED's

#import threading
from threading import Thread
import sys

## Sense hat inits
from sense_hat import SenseHat

sense = SenseHat()
sense.set_rotation(180)

## Serial stuff

ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

power_key = 6
rec_buff = ''
rec_buff2 = ''
time_count = 0

starting = 0
## Patterns for LED Matrix

X = [255, 0, 0]  # Red
O = [0, 0, 0]  # White
L = [0, 255, 0]  # Lime
G = [0, 100, 0] # Green


question_mark = [
    O, O, O, X, X, O, O, O,
    O, O, X, O, O, X, O, O,
    O, O, O, O, O, X, O, O,
    O, O, O, O, X, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, X, O, O, O, O
]

green_checkmark = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, L, O,
    O, O, O, O, O, L, G, O,
    O, O, O, O, O, L, G, O,
    O, G, L, O, L, G, O, O,
    O, O, G, L, G, O, O, O,
    O, O, O, G, O, O, O, O,
    O, O, O, O, O, O, O, O
]

fault = [
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
]

class LedThread(Thread):

    def __init__(self):
        super(LedThread, self).__init__()
        self.variable = None
        self._keepgoing = True

    def run(self):
        while (self._keepgoing):
            if self.variable == "yellow":
                for i in range(0, 255):
                    AR = i
                    Y = [AR, AR, 0]  # Yellow
                    for ffs in range(8):
                        for z in range(8):
                            sense.set_pixel(ffs, z, Y)

                for i in range(255, 0, -1):
                    AR = i
                    Y = [AR, AR, 0]  # Yellow
                    for ra in range(8):
                        for z in range(8):
                            sense.set_pixel(ra, z, Y)

            elif self.variable == "red":
                for i in range(0, 255):
                    AR = i
                    Y = [AR, 0, 0]  # Yellow
                    for ffs in range(8):
                        for z in range(8):
                            sense.set_pixel(ffs, z, Y)

                for i in range(255, 0, -1):
                    AR = i
                    Y = [AR, 0, 0]  # Yellow
                    for ra in range(8):
                        for z in range(8):
                            sense.set_pixel(ra, z, Y)

    def stop(self):
        self._keepgoing = False


def send_at(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' ERROR')
            print(command + ' back:\t' + rec_buff.decode())
            return 0
        else:
            print(rec_buff.decode())

            ## Green checkmark for confirmation
            sense.set_pixels(green_checkmark)
            ## Add the data of GPS to .csv file
            with open("test_data.csv", "a") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow([time.time(),  rec_buff.decode()])


            return 1
    else:
        print('GPS is not ready')

        return 0

def get_gps_position():
    rec_null = True
    answer = 0
    print('Start GPS session...')
    rec_buff = ''
    send_at('AT+CGPS=1,1','OK',1)
    time.sleep(2)
    while rec_null:
        answer = send_at('AT+CGPSINFO','+CGPSINFO: ',1)
        if 1 == answer:
            answer = 0
            if ',,,,,,' in rec_buff:
                print('GPS is not ready')
            sense.set_pixels(question_mark)
            rec_null = False
            time.sleep(1)
        else:
            print('error %d'%answer)
            rec_buff = ''
            send_at('AT+CGPS=0','OK',1)
            return False
        time.sleep(1.5)




def power_on(power_key):
    # When powering on start blink in second Thread
    # flashing_thread = Thread2(target=led_pulse)
    # flashing_thread.start()
    mythread = LedThread()
    mythread.start()
    mythread.variable = "yellow"

    print('SIM7600X is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(20)
    ser.flushInput()
    print('SIM7600X is ready')

    # Stop flashing thread
    # flashing_thread.stop()
    mythread.stop()


def power_down(power_key):
    print('SIM7600X is loging off:')

    mythread = LedThread()
    mythread.start()
    mythread.variable = "red"

    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(3)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(18)
    print('Good bye')

    mythread.stop()

try:
    power_on(power_key)
    get_gps_position()
    power_down(power_key)


except:
    if ser != None:
        ser.close()
    power_down(power_key)
    GPIO.cleanup()
if ser != None:
        ser.close()
        GPIO.cleanup()

