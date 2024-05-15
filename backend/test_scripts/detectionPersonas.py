import cv2
from ultralytics import YOLO
import time

def main():

    model = YOLO("yolov8s.pt") 

    # Iniciar la captura de video
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error al abrir la cámara.")
        return

    try:
        while True:
            # Captura un frame de la cámara
            ret, frame = cap.read()
            if not ret:
                print("Error al capturar video.")
                break

            # Realiza la detección
            results = model(frame)

            # Corrected way to extract information
            bboxes = results.xyxy[0]  # xyxy format bounding boxes
            labels = [results.names[int(cls)] for cls in results.pred[0][:, 5]]
            confidences = results.pred[0][:, 4]  # Extract confidence scores

            # Now, you iterate like this to draw your bounding boxes and put text
            for *xyxy, conf, cls in results.xyxy[0]:
                label = results.names[int(cls)]
                xyxy = [int(x) for x in xyxy]  # Convert tensor to int
                cv2.rectangle(image, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                cv2.putText(image, f'{label}: {conf:.2f}', (xyxy[0], xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow('Object Detection', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print(results)
            #Dibuja los resultados de la detección en el frame
            
            for det in results[0].boxes.numpy():
                # det is now a single detection with attributes you can directly access
                xmin, ymin, xmax, ymax = det.xyxy[0]  # Coordinates
                xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
                conf = det.conf  # Confidence
                cls = det.cls  # Class ID
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(frame, 'Persona', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

                #print(f"Box coordinates: {xmin}, {ymin}, {xmax}, {ymax}, Confidence: {conf}, Class ID: {cls}")

            # for result in results.data:
            #     print(result)
                
            #     xmin, ymin, xmax, ymax = int(result), int(result), int(result), int(result)
            #     cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            #     cv2.putText(frame, 'Persona', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            # Muestra el frame
            cv2.imshow('YOLO Person Detection', frame)

            # Interrumpe si se presiona 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            time.sleep(5)

    finally:
        # Libera la cámara y cierra todas las ventanas
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
