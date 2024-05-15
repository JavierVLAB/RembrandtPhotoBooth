import cv2
from ultralytics import YOLO
import time

def main():

    model = YOLO("yolov8s.pt") 

    # Iniciar la captura de video
    cap = cv2.VideoCapture(0)

    try:
        while True:

        # Captura un frame de la cámara
            ret, frame = cap.read()

            # Realiza la detección
            results = model(frame)

            print("--------")
            #print(results[0].boxes.data.numpy())
            print("-----------")

            for res in results[0].boxes.data.numpy():
                #print(res)
                xmin, ymin, xmax, ymax, cof, cls = res  
                xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(frame, results[0].names[cls], (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            # Muestra el frame
            cv2.imshow('YOLO Person Detection', frame)

            
            time.sleep(5)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
  
    finally:
        # Libera la cámara y cierra todas las ventanas
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
