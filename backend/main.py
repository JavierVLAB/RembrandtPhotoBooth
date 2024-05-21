from fastapi import FastAPI, WebSocket, Response, WebSocketDisconnect
import cv2
import base64
import asyncio
from fastapi.middleware.cors import CORSMiddleware 
from ultralytics import YOLO
import numpy as np
import time
from comfyui_utilities import get_images
from upload_image_FS import upload_image_to_firebase
from datetime import datetime


###########

time_before_photo = 3 #seconds
time_to_see_qr_code = 5 

#cam = {"name": "webMac", "portrait": False, "w": 1280, "h": 720}
cam = {"name": "javiCam", "portrait": True, "w": 1920, "h": 1080}

debug = True
###########

time_now = None
formatted_date = None



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
    img = cv2.resize(img, (960,1200))
    #return cropped_image
    return image

def face_is_center(center, size, points):

    # for point in points:
    #     if np.linalg.norm(center - point) > size:
    #         return False
    
    for point in points:
        if point[0] > center[0] + size or point[0] < center[0] - size or point[1] > center[1] + size or point[1] < center[1] - size:  
            return False
    return True

take_picture_1 = False
take_picture_2 = False        

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
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        
        while True:

            ret, frame = camera.read()   


            if ret:
                #print(frame.shape)
                # mirror  
                frame = cv2.flip(frame, 1)

                #crop
                frame = frame[0:1080,285:1635] if cam['portrait'] else frame[ 0:720, 72:648]
                
                #rotate only the rotated camera
                if cam["portrait"]: frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                    
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

                    #print(frame.shape)
                    (frame_height, frame_width, _) = frame.shape
                    
                    center = (frame_width/2, frame_height*0.4)
                    size = int(frame_width*0.2)
                    colors = None



                    # Determine if the face is inside the circle
                    if face_is_center(center, size, [eyeL_center, eyeR_center]):

                        if counting_time:
                            
                            elapse_time = time.time() - start_time 

                            # if elapse_time > 1 and elapse_time < 2 and take_picture_1:
                            #     cv2.imwrite('images/img{}01.jpg'.format(formatted_date), frame)
                                

                            if elapse_time >= time_before_photo:
                                take_picture = True
                                counting_time = False
       
                        else:

                            await websocket.send_text("text_message:show counter")
                            counting_time = True
                            start_time = time.time()
                            time_now = datetime.now()
                            formatted_date = time_now.strftime('%Y%m%d%H%M%S')

            
                        colors = (0,255,0)
                    else:

                        if counting_time:
                            await websocket.send_text("text_message:hide counter")

                        counting_time = False
                        colors = (0,0,255)

                        

                    if debug:

                        cv2.circle(frame, (int(nose_center[0]),int(nose_center[1])), 3, (255,0,0) , 2)
                        cv2.circle(frame, (int(eyeR_center[0]),int(eyeR_center[1])), 3, (255,0,0) , 2)
                        cv2.circle(frame, (int(eyeL_center[0]),int(eyeL_center[1])), 3, (255,0,0) , 2)
                        cv2.circle(frame, (int(earR_center[0]),int(earR_center[1])), 3, (255,0,0) , 2)
                        cv2.circle(frame, (int(earL_center[0]),int(earL_center[1])), 3, (255,0,0) , 2)
                        
                        cv2.circle(frame, (int(center[0]),int(center[1])), size, colors , 1)
                        cv2.rectangle(frame, (int(center[0] - size),int(center[1] - size)), (int(center[0]+size),int(center[1]+size)), colors , 1)
                        


                    #img = prepare_image(frame)
                    img = frame

                    jpg_as_text = None

                    if take_picture:

                        cv2.imwrite('images/img{}.jpg'.format(formatted_date), frame)
                        
                        time.sleep(0.1)

                        jpg_as_text = await get_images(websocket, 'img{}'.format(formatted_date))        #53 is the node save image in the comfyui workflow

                        image_base64 = base64.b64encode(jpg_as_text).decode('utf-8')

                        time.sleep(0.1)
                        
                        image_out_url = None#upload_image_to_firebase('images_out/img{}out_00001_.png'.format(formatted_date),'imagenes/img{}_out.jpg'.format(formatted_date))

                        take_picture = False

                        await websocket.send_text(image_base64)
                        await asyncio.sleep(0.1) 

                        await websocket.send_text("text_message:image_url:{}".format(image_out_url))
                        await asyncio.sleep(time_to_see_qr_code)
                    
                    _, buffer = cv2.imencode('.jpg', img)
                    
                    jpg_as_text = base64.b64encode(buffer).decode()
                    
                    await websocket.send_text(jpg_as_text)
                    
                    await asyncio.sleep(0.05) 

                else:
                    await websocket.send_text("text_message:No people detected")
                    await asyncio.sleep(2) 
                
            else:
                break

    except WebSocketDisconnect:
        camera.release()
        await websocket.close()



@app.on_event("shutdown")
async def shutdown_event():
    pass



