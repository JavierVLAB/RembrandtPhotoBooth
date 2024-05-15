from fastapi import FastAPI, WebSocket, Response, WebSocketDisconnect
import cv2
import base64
import asyncio
from fastapi.middleware.cors import CORSMiddleware 
from ultralytics import YOLO
import time

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

model = YOLO("yolov8s.pt") 

camera = None

def detect_people(frame):

    results = model(frame)

    for res in results[0].boxes.data.numpy():
        xmin, ymin, xmax, ymax, cof, cls = res  

        if cls == 0:
            return True

    return False

def prepare_image(image):
    # Cropping an image
    width =  image.shape[1]/2
    height = image.shape[0]/2
    cropped_image = image[width-200:width+200, height-300:height+300]
    img = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.resize(img, (400,600))
    return cropped_image

# Endpoint para iniciar la detección y el streaming
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    global camera

    try:
        camera = cv2.VideoCapture(0) 
        while True:

            ret, frame = camera.read()
            if ret:
                if detect_people(frame):
                    img = prepare_image(frame)
                    _, buffer = cv2.imencode('.jpg', img)
                    
                    #await websocket.send_bytes(buffer.tobytes())
                    
                    jpg_as_text = base64.b64encode(buffer).decode()
                    await websocket.send_text(jpg_as_text)
                    
                    await asyncio.sleep(0.05) 

                else:
                    await websocket.send_text("No people detected")
                    await asyncio.sleep(2.5) 
                
            else:
                break

    except WebSocketDisconnect:
        camera.release()
        await websocket.close()

@app.on_event("shutdown")
async def shutdown_event():
    pass
