import cv2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import threading

# Define a class to manage the camera operations
class CameraManager:
    def __init__(self):
        self.cap = None
        self.is_active = False

    def start_camera(self):
        if not self.is_active:
            self.cap = cv2.VideoCapture(0)  # Assuming 0 is the default camera
            if not self.cap.isOpened():
                raise Exception("Cannot open camera")
            self.is_active = True
        else:
            raise Exception("Camera already started")

    def stop_camera(self):
        if self.is_active and self.cap.isOpened():
            self.cap.release()
            self.is_active = False
        else:
            raise Exception("Camera is not active")

    def capture_frame(self):
        if self.is_active and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Can't receive frame (stream end?). Exiting ...")
            return frame
        else:
            raise Exception("Camera is not active")

    def is_running(self):
        return self.is_active

# Define the FastAPI app
app = FastAPI()
camera_manager = CameraManager()

# Define routes for camera control
@app.post("/start")
async def start_camera():
    try:
        camera_manager.start_camera()
        return {"message": "Camera started successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop")
async def stop_camera():
    try:
        camera_manager.stop_camera()
        return {"message": "Camera stopped successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    return {"camera_active": camera_manager.is_running()}

# Commenting out the following lines to prevent actual execution in the PCI
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
