from fastapi import FastAPI, WebSocket, Response, WebSocketDisconnect
import cv2
import base64
import asyncio
from fastapi.middleware.cors import CORSMiddleware 
from ultralytics import YOLO

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_yolo = YOLO('yolov8n.pt')

camera = None

def start_camera():
    global camera
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(0)  # open the camera

    print("camera opened")
    return camera

def stop_camera():
    global camera
    if camera and camera.isOpened():
        camera.release()
        camera = None
    print("Camera released")

def prepare_image(image):
    img = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.resize(img, (400,600))
    return img

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        camera = start_camera() 
        while True:
            ret, frame = camera.read()

            image = prepare_image(frame)
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', image)
            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.01)

    except WebSocketDisconnect:
        print("Client disconnected")
        stop_camera()  # Detener la cámara cuando el cliente se desconecte
        await websocket.close()

@app.on_event("shutdown") 
def shutdown_event():
    #Asegurarse que la camara se apaga al apagar el servidor
    stop_camera() 


@app.post("/take-photo")
async def take_photo():
    #global camera
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()

    ret, frame = camera.read()
    detections = model_yolo(frame)
    #print("-----------------")
    ##print(detections[0].boxes)

    for cls in detections[0].boxes.cls:
        if cls == 0:
            print("Person detected")
    
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv2.resize(frame, (400,600))
    
    if ret:
        # Procesamiento de OpenCV (simulado por ahora)
        _, buffer = cv2.imencode('.jpg', frame)

        return Response(content=buffer.tobytes(), media_type="image/jpeg")
    return {"error": "Failed to capture image"}

