#SIFT y SURF son algoritmos patentados
# Solicitan pago para uso comercial

import cv2
import numpy as np

template = cv2.imread("images/banano_base.jpeg", 0)
cv2.imshow("Template", template)

sift = cv2.xfeatures2d.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(template, None)
template = cv2.drawKeypoints(template, keypoints, None)

cv2.imshow("SIFT Keypoints", template)
#cv2.waitKey(0)

surf = cv2.xfeatures2d.SURF_create()
keypoints, descriptors = surf.detectAndCompute(template, None)
template = cv2.drawKeypoints(template, keypoints, None)

cv2.imshow("SURF Keypoints", template)

orb = cv2.ORB_create(nfeatures = 500)
keypoints, descriptors = orb.detectAndCompute(template, None)
template = cv2.drawKeypoints(template, keypoints, None)

cv2.imshow("ORB Keypoints", template)
cv2.waitKey(0)

#target = cv2.imread("images/banano_m.jpg", 0)
#cv2.imshow("Entrada", target)


cv2.destroyAllWindows()