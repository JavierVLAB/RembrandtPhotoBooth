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


# TO-DO

- ~~ajustar relacion de aspecto camaras~~
- ~~ajustar balance de blanco~~
- ~~como poner los logos~~ poner los logos, esta listo el proceso falta los logos
- ~~mejorar lo del posicionamiento de la cara~~ poner quizas texto de posicionar ojos
- ~~decidir si son los ojos, cara, o etc y arreglarlo~~  la zona esta con los ojos
- ~~como hacer confirmación o simplemente~~
- ~~revisar tiempos de espera ahora: 5 segundos para QR, 3 para toma de foto, 10 para generar IA ~~
- ~~mostrar avance de generacion?~~
- ~~mostrar conteo poner conteo cuando va~~
- ~~mostrar flash poner flash cuando va~~
- ~~arreglar IA~~
- ~~automatizar cambio de camaras y decidir que camara usar~~
- ~~revisar porque despues de ver la nueva imagen se pone primero la foto anterior y luego empieza de nuevo el streaming~~
- ~~Resolver lo de fullscreen~~ ha sido muy complicado
- ~~ver porque no se ve el area al principio~~
- ~~se queda pegado el QR~~
- revisar errores a largo plazo
- pensar en como usar Telegram si se quiere
- Escribir una explicacion de como funciona, y un FAQ
- ~~borrar imagenes local~~
- ~~borrar imagenes nube ~~
- Crear un backup de imagenes de la gente y de los resultados