import cv2
import numpy as np
import json
import os

# Variable para tomar la foto de referencia
take_picture = False  # Cambia esto a False después de tomar la referencia

# Archivo JSON donde se guardarán los valores del balance de blancos
json_file = "white_balance_values.json"

def save_white_balance_values(gains, json_file):
    with open(json_file, 'w') as file:
        json.dump(gains, file)

def load_white_balance_values(json_file):
    with open(json_file, 'r') as file:
        gains = json.load(file)
    return gains

def calculate_white_balance(image):
    result = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])

    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)

    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

def apply_white_balance(image, gains):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    a = cv2.add(a, gains['avg_a'] - 128)
    b = cv2.add(b, gains['avg_b'] - 128)
    updated_lab = cv2.merge([l, a, b])
    balanced_image = cv2.cvtColor(updated_lab, cv2.COLOR_LAB2BGR)
    return balanced_image


if __name__ == "__main__":
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)

    if take_picture:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Reference Image", frame)
            cv2.waitKey(0)  # Espera una tecla para continuar

            # Realiza el balance de blancos en la imagen de referencia
            balanced_frame = calculate_white_balance(frame)

            # Calcula los valores de balance de blancos
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            avg_a = np.average(lab[:, :, 1])
            avg_b = np.average(lab[:, :, 2])
            gains = {
                'avg_a': avg_a,
                'avg_b': avg_b
            }
            save_white_balance_values(gains, json_file)

            # Guarda la imagen de referencia
            cv2.imwrite("reference_image.jpg", balanced_frame)
            cv2.destroyAllWindows()

    else:
        if not os.path.exists(json_file):
            raise FileNotFoundError("No se encontró el archivo de valores de balance de blancos.")

        gains = load_white_balance_values(json_file)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Aplica el balance de blancos usando los valores guardados
            balanced_frame = apply_white_balance(frame, gains)

            # Muestra el video en vivo con el balance de blancos corregido
            cv2.imshow("Live Stream with White Balance", balanced_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Libera la cámara y cierra las ventanas
    cap.release()
    cv2.destroyAllWindows()
