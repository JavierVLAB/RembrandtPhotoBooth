import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('../images/img05221246.jpg')

# Crear el objeto de balance de blancos
wb = cv2.xphoto.createGrayworldWB()

# Aplicar el balance de blancos
balanced_image = wb.balanceWhite(image)

# Mostrar las imágenes original y balanceada
cv2.imshow('Original Image', image)
cv2.imshow('White Balanced Image', balanced_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
