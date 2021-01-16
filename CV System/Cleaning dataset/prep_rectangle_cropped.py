# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:10:27 2021

@author: bniet
"""

import imutils
from os import listdir
from os.path import isfile, join
import numpy as np
from matplotlib import pyplot as plt
from statistics import mean, median
from joblib import load
from LocalBinaryPattern import LocalBinaryPatterns
import cv2


# Detection using pre trained model
def binClassifier(phase, input_image):
    #cv2.imshow(phase, input_image)
    decoding = {
        0: "Non banana",
        1: "Banana"
    }
    radius = 3
    no_points = 8 * radius
    desc = LocalBinaryPatterns(no_points, radius)
    image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    hist = desc.describe(image)
    hist = np.array(hist)
    model = load('../Detecting banano/classifier.joblib')
    prediction = model.predict(hist.reshape(1, -1))
    print("Phase: {0} -->  Prediction: {1}".format(phase, decoding[prediction[0]]))
    return prediction

# ---------------- Finding Object to crop it -----------------------------
def binMask(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Gray', gray)
    
    blur = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
    #cv2.imshow('Blured', blur)
    
    canny = cv2.Canny(blur, 50, 150)
    #cv2.imshow('Edges', canny)
    
    pts = np.argwhere(canny > 0)
    y1, x1 = pts.min(axis=0)
    y2, x2 = pts.max(axis=0)
    cropped = img[y1:y2, x1:x2]

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
   
    return cropped

def main(sourcepath, outputpath):
    print(outputpath)
    #cv2.namedWindow('Entrada', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('Entrada', 450,450)
    #cv2.imshow("Entrada", img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    onlyfiles = [f for f in listdir(sourcepath) if(isfile(join(sourcepath, f)))]
    count = 0
    for i, files in enumerate(onlyfiles):
        if(".jpg" in onlyfiles[i]):
            image_path = sourcepath + files
            #print("{0} => {1}".format(i, image_path))

            img = cv2.imread(image_path)
            img = cv2.resize(img, (150, 150))

            if(img is None):
                print('Could not open or find the images')
                exit(0)

            detector = binClassifier('Full image', img.copy())
            if(detector):
                cropped = binMask(img.copy())
                cv2.imwrite(outputpath + str(count) + ".jpg" , cropped)
                count += 1
                
            else:
                print("No se han encontrado similitudes")
                print("pasando al siguiente...")
    print("finalizado, dataset limpio")

main('../Captured images/Second Try Dataset (green banana)/', './Cleared images/Green banana/')
main('../Captured images/Third Try Dataset (green segment)/', './Cleared images/Green segment/')
main('../Captured images/Sixth (grocery banana segment)/', './Cleared images/Market segment/')