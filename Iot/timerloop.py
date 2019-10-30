# -*- coding: utf-8 -*-
import time
from datetime import datetime
import picamera
from mongoAtlas import MongoConnection 
timer = 10
count = 0

while True:
        now = datetime.now().time()
        current_time = now.strftime("%H:%M:%S")
        if(current_time == "00:00:00" or current_time == "06:00:00"  or current_time == "12:00:00" or current_time == "18:00:00"):
                print("Activating Camera")
                with picamera.PiCamera() as picam:
                        picname = 'pic'+ str(count) +'.jpg'
                        picam.capture('images/'+picname)
                        MongoConnection('images/'+picname)
                        #time.sleep(timer)
                        count += 1
                        picam.close()
                print("Closing Camera")

