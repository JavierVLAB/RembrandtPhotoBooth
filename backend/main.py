from fastapi import FastAPI, WebSocket, Response, WebSocketDisconnect
import cv2
import base64
import asyncio
from fastapi.middleware.cors import CORSMiddleware 
from ultralytics import YOLO
import numpy as np
import time
from comfyui_utilities import generate_image
from upload_image_FS import upload_image_to_firebase
from datetime import datetime
from insertpngopenCV import insert_logos


###########

time_before_photo = 3 #seconds
time_to_see_qr_code = 5 

#cam = {"name": "webMac", "portrait": False, "w": 1280, "h": 720}
cam = {"name": "javiCam", "portrait": True, "w": 1920, "h": 1080}

debug = False
###########

time_now = None
formatted_date = None

app = FastAPI()
 
# Esto permite CORS
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

# Modelo para detectar la persona, esto da los puntos de la cara
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

    # # mira si los puntos dentro del circulo centrado en center y de radio size
    # for point in points:
    #     if np.linalg.norm(center - point) > size:
    #         return False
    
    # mira si los puntos estan en el recuadro centrado en center y de tamaño 2 size
    for point in points:
        if point[0] > center[0] + size or point[0] < center[0] - size or point[1] > center[1] + size or point[1] < center[1] - size:  
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

        # Aseguramos que la camara este a 1920x1080 
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        
        while True:

            ret, frame = camera.read()   

            if ret:
                
                # mirror  
                frame = cv2.flip(frame, 1) 

                #crop Cortamos para estar justo a 4/5 de relacion de aspecto
                frame = frame[0:1080,285:1635] if cam['portrait'] else frame[ 0:720, 72:648]
                
                #rotate only the rotated camera
                if cam["portrait"]: frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                    
                # detectamos las personas    
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

                    (frame_height, frame_width, _) = frame.shape
                    
                    # Definimos center y tamaño de posicion para los ojos
                    center = (frame_width/2, frame_height*0.4)
                    size = int(frame_width*0.2)
                    colors = None

                    # Determine if the face is inside of the area
                    if face_is_center(center, size, [eyeL_center, eyeR_center]):

                        if counting_time:
                            
                            elapse_time = time.time() - start_time  

                            # Wait for X before take the photo
                            if elapse_time >= time_before_photo:
                                take_picture = True
                                counting_time = False
       
                        else:
                            #The first time eye are in the area we activate the counter
                            await websocket.send_text("text_message:show counter")
                            counting_time = True
                            start_time = time.time()

                            # Definition of the name of the file (month day, hour and minute)
                            time_now = datetime.now()
                            formatted_date = time_now.strftime('%m%d%H%M')

            
                        colors = (0,255,0)
                    else:

                        if counting_time:
                            # if eye are out of the area we stop the counter
                            await websocket.send_text("text_message:hide counter")

                        counting_time = False
                        colors = (0,0,255)

                    # Show the area for the eyes and the point in the body (nose and eyes)
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

                        take_picture = False

                        # Guardamos la imagen
                        cv2.imwrite('images/img{}.jpg'.format(formatted_date), frame)
                        
                        time.sleep(0.1)

                        # Generamos la nueva imagen con la IA
                        await generate_image(websocket, 'img{}'.format(formatted_date))        #53 is the node save image in the comfyui workflow

                        #image_base64 = base64.b64encode(jpg_as_text).decode('utf-8')

                        time.sleep(0.1)
                        
                        # Insertamos los logos
                        insert_logos('images_out/img{}out_00001_.png'.format(formatted_date), 'images_out/img{}_out.png'.format(formatted_date))

                        time.sleep(0.1)

                        # Enviamos la imagen a firebase
                        image_out_url = None #upload_image_to_firebase('images_out/img{}_out.png'.format(formatted_date),'imagenes/img{}_out.png'.format(formatted_date))
                        
                        # Preparamos la imagen para enviarla a Nextjs
                        send_img = cv2.imread('images_out/img{}out.png'.format(formatted_date))
                        _, buffer = cv2.imencode('.jpg', send_img)
                        jpg_as_text = base64.b64encode(buffer).decode()

                        await websocket.send_text(jpg_as_text)
                        await asyncio.sleep(0.1) 

                        await websocket.send_text("text_message:image_url:{}".format(image_out_url))
                        await asyncio.sleep(time_to_see_qr_code)
                    
                    # Preparamos la imagen normal para enviarla a Nextjs
                    _, buffer = cv2.imencode('.jpg', img)
                    jpg_as_text = base64.b64encode(buffer).decode()
                    
                    await websocket.send_text(jpg_as_text)
                    await asyncio.sleep(0.05) 

                else:
                    # Si no se detecta a nadie, mandamos el texto de no detection
                    await websocket.send_text("text_message:No people detected") 
                    await asyncio.sleep(5)

                
            else:
                break

    except WebSocketDisconnect:
        camera.release()
        await websocket.close()
    
    finally:
        camera.release()
        await websocket.close()

@app.on_event("shutdown")
async def shutdown_event():
    pass



