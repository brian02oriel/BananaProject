import imutils
import numpy as np
import cv2

img = cv2.imread('images/banano_v2.jpg')
if img is None:
    print('Could not open or find the images')
    exit(0)


img = imutils.resize(img, width = 600)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

verde_bajos = np.array([49,50,50], dtype=np.uint8)
verde_altos = np.array([80, 255, 255], dtype=np.uint8)

#amarillo_bajos = np.array([16,76,72], dtype=np.uint8)
#amarillo_altos = np.array([30, 255, 210], dtype=np.uint8)

#Detectar los pixeles de la imagen que esten dentro del rango de verdes
mascara_verde = cv2.inRange(hsv, verde_bajos, verde_altos)

#Detectar los pixeles de la imagen que esten dentro del rango de amarillos
#mascara_amarillo = cv2.inRange(hsv, amarillo_bajos, amarillo_altos)

#Filtrar el ruido aplicando un OPEN seguido de un CLOSE
kernel = np.ones((6, 6), np.uint8)
mascara_verde = cv2.morphologyEx(mascara_verde, cv2.MORPH_CLOSE, kernel)
mascara_verde = cv2.morphologyEx(mascara_verde, cv2.MORPH_OPEN, kernel)
#mascara_amarillo = cv2.morphologyEx(mascara_amarillo, cv2.MORPH_CLOSE, kernel)
#mascara_amarillo = cv2.morphologyEx(mascara_amarillo, cv2.MORPH_OPEN, kernel)

#Unir las dos mascaras con el comando cv2.add()
#mask = cv2.add(mascara_amarillo, mascara_verde)
#cnts = cv2.findContours(mascara_amarillo.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2]
cnts = cv2.findContours(mascara_verde.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2]

cv2.drawContours(img, cnts, 0, (0, 0, 255), 2)

#Mostrar la mascara final y la imagen
cv2.imshow('mascaras', mascara_verde)
cv2.imshow('Camara', img)
cv2.waitKey(0)
cv2.destroyAllWindows()