# RembrandtPhotoBooth

# Installation

## Backend

Installation on mac or linux

```
% cd backend/
% python3.11 -m venv venv
% source venv/bin/activate
(venv)% pip install -r requirements.txt
```

Installation on Windows

- Using Powershell
- Install virtualenv
- In administrator PowerShell allow local scripts with ```Set-ExecutionPolicy RemoteSigned```

```
% cd backend/
% virtualenv venv
% .\venv\Scripts\activate
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
- Install insightface (https://github.com/Gourieff/comfyui-reactor-node?tab=readme-ov-file#i-for-windows-users-if-you-still-cannot-build-insightface-for-some-reasons-or-just-dont-want-to-install-visual-studio-or-vs-c-build-tools---do-the-following)

download https://huggingface.co/InstantX/InstantID/tree/main/ControlNetModel diffusion_pythorch_model.safetensors
download ip-adapter.bin comfyui
dowload antylope2 https://github.com/deepinsight/insightface/tree/master/python-package

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
cd path/to/ComfyUI
python3.11 main.py --input-directory /Users/javi/Documents/workspace/ThyssenIED/RembrandtPhotoBooth/backend/images/ --output-directory /Users/javi/Documents/workspace/ThyssenIED/RembrandtPhotoBooth/backend/images_out
```

"cd /Users/javi/Documents/workspace/ComfyUI/ComfyUI"

Run ComfyUi indicating the image input dir and the image output dir

# Usage

Open the APP at [http://localhost:3000/prototipo](localhost:3000/prototipo)
