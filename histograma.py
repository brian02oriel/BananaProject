import cv2
import numpy as np
from matplotlib import pyplot as plt

bnaMadura = cv2.imread('images/banano_m.jpeg')
cv2.imshow('banana madura', bnaMadura)
#cv2.waitKey(0)

bnaVerde = cv2.imread('images/banano_v.jpg')
cv2.imshow('banana verde', bnaVerde)
#cv2.waitKey(0)

template = cv2.imread('images/banano_base.jpeg')
cv2.imshow('banano base', template)
#cv2.waitKey(0)

#cv2.destroyAllWindows()
def histo(img):
    color = ('b', 'g', 'r')
    for i, c in enumerate(color):
        hist = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(hist, color = c)
        plt.xlim([0, 256])
    
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def matching(template, img):
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(template_gray, 127, 255, 0)
    ret, thresh2 = cv2.threshold(target_gray, 127, 255, 0)

    _, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    template_contour = contours[1]

    _, contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    print("Contours")
    print(contours)

    for c in contours:
    # cv2.matchShapes(contour1, contour2, method number, parameter)
        match = cv2.matchShapes(template_contour, c, 2, 0.0)
        print("Match")
        print(match)
        if match < 0.15:
            closest_contour = c
        else:
            closest_contour = []
    print("Closest Contours")
    print(closest_contour)
    cv2.drawContours(img, [closest_contour], -1, (0, 255, 0), 3)
    cv2.imshow('Output', img)
    


histo(bnaMadura)
matching(template, bnaMadura)
cv2.waitKey()
cv2.destroyAllWindows()
#histo(bnaVerde)
