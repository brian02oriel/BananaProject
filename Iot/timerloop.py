import time
from datetime import datetime
import picamera

timer = 60000
count = 0

while True:
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        with picamera.PiCamera() as picam:
                #picam.start_preview()
                time.sleep(10)
                picam.capture('images/pic'+ str(count)+'.jpg')
                print('images/pic'+ str(count)+'.jpg created')
                print('Current time :' + current_time)
                #picam.stop_preview()
                picam.close()
                count += 1

