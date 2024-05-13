import cv2
import numpy as np

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    """ Ajusta el brillo y el contraste de la imagen dada """
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
    else:
        buf = image.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

def rembrandt_effect(image_path):
    # Captura de imagen
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to grab frame")
        return

    image = frame.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Ajuste de brillo y contraste
    adjusted = gray#adjust_brightness_contrast(gray, brightness=-30, contrast=30)
    
    # Crear una máscara para simular sombras
    mask = np.zeros_like(adjusted)
    height, width = mask.shape
    cv2.ellipse(mask, (int(width * 0.5), int(height * 0.4)), (int(width * 0.5), int(height * 0.8)), 0, 0, 360, 255, -1)
    blended = cv2.addWeighted(adjusted, 0.5, mask, 0.5, 0)

    # Mostrar la imagen
    cv2.imshow('Rembrandt Effect', blended)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Ejecutar la función
rembrandt_effect('path_to_image')
