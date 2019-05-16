import imutils
import numpy as np
import cv2

img = cv2.imread('images/banano_m.jpg')
if img is None:
    print('Could not open or find the images')
    exit(0)
img = imutils.resize(img, width = 600)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
verde_bajos1 = np.array([0,70,63])
verde_altos1 = np.array([0, 255, 230])

verde_bajos2 = np.array([1,85,61])
verde_altos2 = np.array([0, 255, 182])

verde_bajos3 = np.array([0,70,63])
verde_altos3 = np.array([0, 255, 230])

verde_bajos4 = np.array([0,70,63])
verde_altos4 = np.array([0, 255, 230])

#Rango de colores detectados:
#Verdes:
#verde_bajos = np.array([49,50,50])
#verde_altos = np.array([107, 255, 255])
#Azules:
#azul_bajos = np.array([100,65,75], dtype=np.uint8)
#azul_altos = np.array([130, 255, 255], dtype=np.uint8)

#Rojos:
#rojo_bajos1 = np.array([0,65,75], dtype=np.uint8)
#rojo_altos1 = np.array([12, 255, 255], dtype=np.uint8)
#rojo_bajos2 = np.array([240,65,75], dtype=np.uint8)
#rojo_altos2 = np.array([256, 255, 255], dtype=np.uint8)

#mascara_verde = cv2.inRange(hsv, verde_bajos, verde_altos)
#mascara_rojo1 = cv2.inRange(hsv, rojo_bajos1, rojo_altos1)
#mascara_rojo2 = cv2.inRange(hsv, rojo_bajos2, rojo_altos2)
#mascara_azul = cv2.inRange(hsv, azul_bajos, azul_altos)

#Juntar todas las mascaras
#mask = cv2.add(mascara_rojo1, mascara_rojo2)
#mask = cv2.add(mask, mascara_verde)
#mask = cv2.add(mask, mascara_azul)

_, cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img, [cnts], -1, (255, 0, 255), 3)

#Mostrar la mascara final y la imagen
cv2.imshow('Finale', mask)
cv2.imshow('Imagen', img)

cv2.waitKey()
cv2.destroyAllWindows()
