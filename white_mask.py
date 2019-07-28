import imutils
import numpy as np
import cv2

img = cv2.imread('images/banano_v2.jpg')
if img is None:
    print('Could not open or find the images')
    exit(0)


img = imutils.resize(img, width = 600)


verde_bajos_1 = np.array([228, 228, 228], dtype=np.uint8)
verde_altos_1 = np.array([255, 255, 255], dtype=np.uint8)


#Detectar los pixeles de la imagen que esten dentro del rango de verdes
mascara_verde_1 = cv2.inRange(img, verde_bajos_1, verde_altos_1)

#Filtrar el ruido aplicando un OPEN seguido de un CLOSE
kernel = np.ones((6, 6), np.uint8)
mascara_verde_1 = cv2.morphologyEx(mascara_verde_1, cv2.MORPH_CLOSE, kernel)
mascara_verde_1 = cv2.morphologyEx(mascara_verde_1, cv2.MORPH_OPEN, kernel)

#Unir las dos mascaras con el comando cv2.add()

cnts = cv2.findContours(mascara_verde_1.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2]


cv2.drawContours(img, cnts, 0, (0, 0, 255), 2)

#Mostrar la mascara final y la imagen
cv2.imshow('mascaras', mascara_verde_1)
cv2.imshow('Camara', img)
cv2.waitKey(0)
cv2.destroyAllWindows()