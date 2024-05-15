from fastapi import FastAPI, WebSocket, Response, WebSocketDisconnect
import cv2
import base64
import asyncio
from fastapi.middleware.cors import CORSMiddleware 
from ultralytics import YOLO
import numpy as np
import time

debug = True

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

model = YOLO("models/yolov8n-pose.pt") 

camera = None

def prepare_image(image):
    # Cropping an image
    #print(image.shape) 1280  640 576 288 
    #cropped_image = image[0:720,352:928]
    
    #img = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    #img = cv2.resize(img, (960,1200))
    #return cropped_image
    return image

def face_is_center(center, size, points):

    for point in points:
        if np.linalg.norm(center - point) > size:
            return False
    
    return True
        

# Endpoint para iniciar la detección y el streaming
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    global camera
    start_time = 0
    counting_time = False
    take_picture = False

    try:
        camera = cv2.VideoCapture(0) 
        while True:

            ret, frame = camera.read()   

            # mirror  
            #frame = cv2.flip(frame, 1)
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            if ret:
                results = model(frame, verbose=False)
                
                results_data = results[0].keypoints.data.numpy().shape[1]
                
                #If there is detection results_data > 0
                if results_data > 0:

                    # Keypoint in the detections
                    nose_center = results[0].keypoints.xy.numpy()[0][0]
                    eyeL_center = results[0].keypoints.xy.numpy()[0][1]
                    eyeR_center = results[0].keypoints.xy.numpy()[0][2]
                    earL_center = results[0].keypoints.xy.numpy()[0][3]
                    earR_center = results[0].keypoints.xy.numpy()[0][4]

                    center = (640, 360)
                    size = 100
                    colors = None

                    # Determine if the face is inside the circle
                    if face_is_center(center, size, [eyeL_center, eyeR_center]):
                        
                        if counting_time:
                            
                            if time.time() - start_time >= 3:
                                take_picture = True
                                counting_time = False

                                
                        else:
                            
                            counting_time = True
                            start_time = time.time()
                             
                        colors = (0,255,0)
                    else:
                        counting_time = False
                        colors = (0,0,255)

                    if debug:

                        cv2.circle(frame, (int(nose_center[0]),int(nose_center[1])), 3, (255,0,0) , 2)
                        cv2.circle(frame, (int(eyeR_center[0]),int(eyeR_center[1])), 3, (255,0,0) , 2)
                        cv2.circle(frame, (int(eyeL_center[0]),int(eyeL_center[1])), 3, (255,0,0) , 2)
                        cv2.circle(frame, (int(earR_center[0]),int(earR_center[1])), 3, (255,0,0) , 2)
                        cv2.circle(frame, (int(earL_center[0]),int(earL_center[1])), 3, (255,0,0) , 2)
                        
                        cv2.circle(frame, (640,360), 100, colors , 1)

                    #img = prepare_image(frame)
                    img = frame

                    if take_picture:
                        
                        take_picture = False

                    _, buffer = cv2.imencode('.jpg', img)
                    
                    jpg_as_text = base64.b64encode(buffer).decode()
                    await websocket.send_text(jpg_as_text)
                    
                    await asyncio.sleep(0.05) 

                else:
                    await websocket.send_text("No people detected")
                    await asyncio.sleep(5) 
                
            else:
                break

    except WebSocketDisconnect:
        camera.release()
        await websocket.close()



@app.on_event("shutdown")
async def shutdown_event():
    pass



