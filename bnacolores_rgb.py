import imutils
import numpy as np
import cv2

img = cv2.imread('images/banano_v2.jpg')
if img is None:
    print('Could not open or find the images')
    exit(0)


img = imutils.resize(img, width = 600)
#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

verde_bajos_1 = np.array([0, 51, 23], dtype=np.uint8)
verde_altos_1 = np.array([0, 255, 115], dtype=np.uint8)

verde_bajos_2 = np.array([0, 51, 38], dtype=np.uint8)
verde_altos_2 = np.array([0, 255, 239], dtype=np.uint8)

#amarillo_bajos = np.array([16,76,72], dtype=np.uint8)
#amarillo_altos = np.array([30, 255, 210], dtype=np.uint8)

#Detectar los pixeles de la imagen que esten dentro del rango de verdes
mascara_verde_1 = cv2.inRange(img, verde_bajos_1, verde_altos_1)
mascara_verde_2 = cv2.inRange(img, verde_bajos_2, verde_altos_2)

#Detectar los pixeles de la imagen que esten dentro del rango de amarillos
#mascara_amarillo = cv2.inRange(hsv, amarillo_bajos, amarillo_altos)

#Filtrar el ruido aplicando un OPEN seguido de un CLOSE
kernel = np.ones((6, 6), np.uint8)
mascara_verde_1 = cv2.morphologyEx(mascara_verde_1, cv2.MORPH_CLOSE, kernel)
mascara_verde_1 = cv2.morphologyEx(mascara_verde_1, cv2.MORPH_OPEN, kernel)

mascara_verde_2 = cv2.morphologyEx(mascara_verde_2, cv2.MORPH_CLOSE, kernel)
mascara_verde_2 = cv2.morphologyEx(mascara_verde_2, cv2.MORPH_OPEN, kernel)

#mascara_amarillo = cv2.morphologyEx(mascara_amarillo, cv2.MORPH_CLOSE, kernel)
#mascara_amarillo = cv2.morphologyEx(mascara_amarillo, cv2.MORPH_OPEN, kernel)

#Unir las dos mascaras con el comando cv2.add()
mask = cv2.add(mascara_verde_1, mascara_verde_2)
cnts = cv2.findContours(mask.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2]
#cnts = cv2.findContours(mascara_verde.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2]

cv2.drawContours(img, cnts, 0, (0, 0, 255), 2)

#Mostrar la mascara final y la imagen
#cv2.imshow('mascaras', mascara_verde)
cv2.imshow('mascaras', mask)
cv2.imshow('Camara', img)
cv2.waitKey(0)
cv2.destroyAllWindows()