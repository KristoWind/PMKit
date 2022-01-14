from sense_hat import SenseHat, ACTION_RELEASED
import pygame
import time
import subprocess
import os
from threading import Thread
from ledmatrix import question_mark, green_checkmark

pygame.init()
screen = pygame.display.set_mode((0,0))


sense = SenseHat()
event = sense.stick.wait_for_event()

startPreview = '/home/pi/Desktop/start.sh'
status = 0

filename = time.strftime("%Y_%m_%d-%I_%M_%S_%p")

class RecordingThread(Thread):
    def __init__(self):
        super(RecordingThread, self).__init__()
        self._keepgoing = True

    def run(self):
        while self._keepgoing:
            #subprocess.Popen("ffmpeg -f v4l2 -i /dev/video0 -c:v copy -c:a copy /media/pi/storage/video_" + filename + ".mkv")
            #subprocess.Popen(["ffmpeg", "-f v4l2 -i /dev/video0 -c:v copy -c:a copy /media/pi/storage/video_" + filename + ".mkv"])
            subprocess.Popen(["ffmpeg -f v4l2 -i /dev/video0 -c:v copy -c:a copy /media/pi/storage/video_" + filename + ".mkv"])
    def stop(self):
        os.system("pkill ffmpeg")
        self._keepgoing = False


recordthread = RecordingThread()
test = 0
def clamp(value, min_value=0, max_value=5):
    return min(max_value, max(min_value, value))

def pushed_middle(event):
    if event.action != ACTION_RELEASED:
        global status
        status = clamp(status + 1)

def refresh():
    global status
    if status == 0:
        print("0")
        sense.set_pixels(question_mark)
    elif status == 1:
        for i in range(1):
            print("1")
            os.system(startPreview)
    elif status == 2:
        for i in range(1):
            print("2")
            os.system("pkill mplayer")
            print("Starting Recording in 2 sec!")
            time.sleep(2)
            recordthread.start()
    elif status == 4:
        for i in range(1):
            print("4")
            sense.clear()
            pygame.quit()
            recordthread.stop()


sense.stick.direction_middle = pushed_middle
sense.stick.direction_any = refresh
refresh()




