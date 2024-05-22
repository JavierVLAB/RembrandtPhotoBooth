@echo off
start "" "C:\Users\User\RembrandtPhotoBooth\init_fastapi.bat"
start "" "C:\Users\User\RembrandtPhotoBooth\init_comfyui_nvidia.bat"
start "" "C:\Users\User\RembrandtPhotoBooth\init_nextjs.bat"
timeout /t 10 /nobreak >nul
start "" "C:\Users\User\RembrandtPhotoBooth\init_darkroom_app.bat"
exit
