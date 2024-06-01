import cv2
import numpy as np

# Función para calcular el brillo medio de una imagen
def calculate_brightness(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    brightness = np.mean(hsv[:, :, 2])
    return brightness


if __name__ == "__main__":

    # Inicializar la cámara
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se puede abrir la cámara")
        exit()



    # Configuración inicial de la cámara
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # Capturar frame por frame
        ret, frame = cap.read()
        
        if not ret:
            print("No se puede recibir frame (stream end?). Saliendo ...")
            break

        # Calcular el brillo de la imagen
        brightness = calculate_brightness(frame)
        print(f"Brillo medio: {brightness}")

        # Ajustar el brillo de la cámara en función del brillo calculado
        if brightness < 50:
            cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.6)
        elif brightness < 100:
            cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
        elif brightness < 150:
            cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.4)
        else:
            cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.3)
        
        # Mostrar el frame
        cv2.imshow('Frame', frame)

        # Salir del bucle si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar los recursos
    cap.release()
    cv2.destroyAllWindows()


