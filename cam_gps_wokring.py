import RPi.GPIO as GPIO
import serial, time, csv
from ledmatrix import question_mark, green_checkmark

# Import threading
from threading import Thread

# Sense hat inits
from sense_hat import SenseHat

# Sense hat initialisation
sense = SenseHat()
sense.set_rotation(180)

## Serial stuff for GPS module
ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

power_key = 6
rec_buff = ''
rec_buff2 = ''
time_count = 0
starting = 0





class LedThread(Thread):

    def __init__(self):
        super(LedThread, self).__init__()
        self.variable = None
        self._keepgoing = True

    def run(self):
        while (self._keepgoing):
            # If you set color to yellow
            if self.variable == "yellow":
                # Fade in
                for i in range(0, 255):
                    color_intensity = i
                    color = [color_intensity, color_intensity, 0]  # Yellow

                    # Set all display pixels 8x8
                    for x_yellow in range(8):
                        for y_yellow in range(8):
                            sense.set_pixel(x_yellow, y_yellow, color)

                # Fade out
                for i in range(255, 0, -1):
                    color_intensity = i
                    color = [color_intensity, color_intensity, 0]  # Yellow

                    # Set all display pixels 8x8
                    for x_yellow2 in range(8):
                        for y_yellow2 in range(8):
                            sense.set_pixel(x_yellow2, y_yellow2, color)


            # If you set color to red
            elif self.variable == "red":
                # Fade in
                for i in range(0, 255):
                    color_intensity = i
                    color = [color_intensity, 0, 0]  # Red

                    # Set all display pixels 8x8
                    for x_red in range(8):
                        for y_red in range(8):
                            sense.set_pixel(x_red, y_red, color)
                # Fade out
                for i in range(255, 0, -1):
                    color_intensity = i
                    color = [color_intensity, 0, 0]  # Red

                    # Set all display pixels 8x8
                    for x_red2 in range(8):
                        for y_red2 in range(8):
                            sense.set_pixel(x_red2, y_red2, color)

    def stop(self):
        self._keepgoing = False



# GPS receive and write to csv

def send_at(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)


    if ser.inWaiting():
        time.sleep(0.1)
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' ERROR')
            print(command + ' back:\t' + rec_buff.decode())
            return 0
        else:
            print(rec_buff.decode())

            # Green checkmark for confirmation
            sense.flip_h()
            sense.set_pixels(green_checkmark)
            # Add the data of GPS to .csv file
            with open("/media/pi/storage/GPSdata.csv", "a") as f:
                writer = csv.writer(f, delimiter=",")
                # TODO change rec_buff naar alleen locatie.
                # kan met []
                writer.writerow([time.time(),  rec_buff.decode()])


            return 1
    else:
        # error here
        #TODO FIX THIS SHIT
        print('GPS is not ready 1')
        return 0

def get_gps_position():
    rec_null = True
    answer = 0
    print('Start GPS session...')
    rec_buff = ''
    #send_at('AT+CGPS=1','OK',1)
    send_at('AT+CGPS=1,1', 'OK', 1)
    time.sleep(0.5)
    while rec_null:
        answer = send_at('AT+CGPSINFO','+CGPSINFO: ',1)
        if 1 == answer:
            answer = 0
            if ',,,,,,,,' in rec_buff:
                print('GPS is not ready 2')
                sense.set_pixels(question_mark)
                #TODO fix question mark when there is no GPS data
                rec_null = False
                time.sleep(1)
        else:
            print('error %d'%answer)
            rec_buff = ''
            send_at('AT+CGPS=0','OK',1)
            return False
        time.sleep(0.1)

def power_on(power_key):
    # When powering on start blink in second Thread
    mythread = LedThread()
    mythread.start()
    mythread.variable = "yellow"

    #print("Recording Started")
    #camera.start_recording('final3.h264')

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
    mythread.stop()

def power_down(power_key):
    mythread = LedThread()
    mythread.start()
    mythread.variable = "red"
    #print("Stopped recording")
    #camera.stop_recording()

    print('SIM7600X is loging off:')

    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(3)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(18)
    print('Good bye')


try:
    power_on(power_key)
    get_gps_position()
    power_down(power_key)


except:
    if ser != None:
        ser.close()
    power_down(power_key)
if ser != None:
        ser.close()
        GPIO.cleanup()
