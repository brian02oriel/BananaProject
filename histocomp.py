import cv2
import numpy as np

base = cv2.imread('images/banano_base.jpeg')
test1 = cv2.imread('images/banano_v.jpg')

if base is None or test1 is None:
    print('Could not open or find the images')
    exit(0)

hsv_base = cv2.cvtColor(base, cv2.COLOR_BGR2HSV)
hsv_test1 = cv2.cvtColor(test1, cv2.COLOR_BGR2HSV)

hsv_half_down = hsv_base[hsv_base.shape[0]//2:,:]


h_bins = 50
s_bins = 60
histSize = [h_bins, s_bins]
# hue varies from 0 to 179, saturation from 0 to 255
h_ranges = [0, 180]
s_ranges = [0, 256]
ranges = h_ranges + s_ranges # concat lists
# Use the 0-th and 1-
channels = [0, 1]

hist_base = cv2.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
cv2.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

hist_half_down = cv2.calcHist([hsv_half_down], channels, None, histSize, ranges, accumulate=False)
cv2.normalize(hist_half_down, hist_half_down, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

hist_test1 = cv2.calcHist([hsv_test1], channels, None, histSize, ranges, accumulate=False)
cv2.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

# 0 = Correlation, 1 = Chi Cuadrado, 2 = Intersection, 3 = Bhattacharyya
method = 3
base_test = cv2.compareHist(hist_base, hist_test1, method)
base_base = cv2.compareHist(hist_base, hist_base, method)

print('Method:', method, 'Base-Test(1): ', base_test)
print('Method:', method, 'Base-Base(1): ', base_base)

if base_test >= 0.0 and base_test <= 0.6:
    print("Existe coincidencia")
    cv2.imshow('Imagen base', base)
    cv2.imshow('Imagen entrada', test1)
else:
    print("Coincidencia insuficiente")
    exit(0)

cv2.waitKey(0)
cv2.destroyAllWindows()

#for compare_method in range(4):
#    base_base = cv2.compareHist(hist_base, hist_base, compare_method)
#    base_half = cv2.compareHist(hist_base, hist_half_down, compare_method)
#    base_test1 = cv2.compareHist(hist_base, hist_test1, compare_method)

#    print('Method:', compare_method, 'Perfect, Base-Half, Base-Test(1): ',\
#          base_base, '/', base_half, '/', base_test1)

