# -*- coding: utf-8 -*-
import time
from datetime import datetime
import picamera
from mongoAtlas import MongoConnection 
timer = 10
count = 0

while True:
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        with picamera.PiCamera() as picam:
                picname = 'pic'+ str(count) +'.jpg'
                picam.capture('images/'+picname)
                picam.close()
                MongoConnection('images/'+picname)
                time.sleep(timer)
                count += 1

