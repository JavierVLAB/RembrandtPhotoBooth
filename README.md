# RembrandtPhotoBooth

# Installation

## Backend

Installation on mac or linux

```
% cd backend/
% python3.11 -m venv venv
% source venv/bin/activate
(venv)% pip install "fastapi[all]"
(venv)% pip install -r requirements.txt
```
## Frontend

```
% cd nextjsfrontend
% npm install
```

## ComfyUI

- Install ComfyUI (https://stable-diffusion-art.com/how-to-install-comfyui/)
- Install ComfyUI Manager (https://github.com/ltdrdata/ComfyUI-Manager)
- Install Was Node (in ComfyUI Manager)
- Install missing nodes (in ComfyUI Manager)
- Install Models IC-light (in ComfyUI Manager)
- Remeber enable the dev mode for save the workflow api

# Execution

## Backend

```
% cd backend
% source venv/bin/activate
(venv)% uvicorn main:app --reload
```

## Frontend

```
% npm run dev
``` 


## ComfyUI

```
cd /ComfyUI/ComfyUI
python3.11 main.py --input-directory /Users/javi/Documents/workspace/ThyssenIED/RembrandtPhotoBooth/backend/images/ --output-directory /Users/javi/Documents/workspace/ThyssenIED/RembrandtPhotoBooth/backend/images_out
```

Run ComfyUi indicating the image input dir and the image output dir

# Usage

Open the APP at [http://localhost:3000/prototipo](localhost:3000/prototipo)