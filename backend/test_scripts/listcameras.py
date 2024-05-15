import cv2

def list_cameras(max_cameras=10):
    cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append(i)
            cap.release()
    return cameras

def main():
    cameras = list_cameras()
    if not cameras:
        print("No se encontraron cámaras.")
        return

    print("Cámaras disponibles:")
    for idx, cam in enumerate(cameras):
        print(f"{idx}: Cámara {cam}")

    cam_idx = int(input("Seleccione el índice de la cámara que desea usar: "))
    if cam_idx < 0 or cam_idx >= len(cameras):
        print("Índice de cámara no válido.")
        return

    selected_camera = cameras[cam_idx]
    cap = cv2.VideoCapture(selected_camera)

    if not cap.isOpened():
        print("No se pudo abrir la cámara seleccionada.")
        return

    print(f"Usando la cámara {selected_camera}. Presione 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el frame.")
            break
        cv2.imshow(f"Cámara {selected_camera}", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
