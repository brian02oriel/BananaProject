import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('images/apple.jpg')

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600,600)

cv2.imshow('image',  img)

if img is None:
    print('Could not open or find the images')
    exit(0)

# img  = cv2.cvtColor( img, cv2.COLOR_BGR2HSV)

def histo(img):
    color = ('b', 'g', 'r')
    plt.figure()

    for i, c in enumerate(color):
        hist = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.subplot(221 + i)
        plt.grid(True)
        plt.plot(hist, color = c)
        plt.xlim([0, 256])
    
    plt.show()


histo( img)
cv2.waitKey(0)
cv2.destroyAllWindows()

