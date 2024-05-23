@echo off

start "" "C:\Users\User\RembrandtPhotoBooth\init\init_comfyui_nvidia.bat"
start "" "C:\Users\User\RembrandtPhotoBooth\init\init_fastapi.bat"
start "" "C:\Users\User\RembrandtPhotoBooth\init\init_nextjs.bat"
start "" "C:\Users\User\RembrandtPhotoBooth\init\clean_images.bat"
timeout /t 30 /nobreak >nul

taskkill /F /IM chrome.exe

timeout /t 5 /nobreak >nul

start "" "C:\Users\User\RembrandtPhotoBooth\init\init_darkroom_app.bat"
exit
