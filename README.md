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
python3.11 main.py
```

# Usage

Open the APP at [http://localhost:3000/prototipo](localhost:3000/prototipo)