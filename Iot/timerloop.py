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
                time.sleep(timer)
                picname = 'pic'+ str(count) +'.jpg'
                picam.capture('images/'+picname)
                MongoConnection('images/'+picname)
                picam.close()
                count += 1

