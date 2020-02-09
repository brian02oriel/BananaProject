# -*- coding: utf-8 -*-
import time
from datetime import datetime
import picamera
from mongoAtlas import MongoConnection 
timer = 1
count = 39

while True:
        now = datetime.now().time()
        current_time = now.strftime("%H:%M:%S")
        if(current_time == "00:00:00" or current_time == "06:00:00"  or current_time == "12:00:00" or current_time == "14:00:00" or current_time == "18:00:00"):
                print("Activating Camera")
                with picamera.PiCamera() as picam:
                        picname = 'pic'+ str(count) +'.jpg'
                        picam.capture('images/'+picname)
                        MongoConnection('images/'+picname)
                        count += 1
                        #time.sleep(timer)
                        picam.close()
                print("Closing Camera")

