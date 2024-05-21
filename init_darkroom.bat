@echo off
start "" "C:\Users\User\RembrandtPhotoBooth\init_fastapi.bat"
start "" "C:\Users\User\RembrandtPhotoBooth\init_comfyui_nvidia.bat"
start "" "C:\Users\User\RembrandtPhotoBooth\init_nextjs.bat"
timeout /t 10 /nobreak >nul
start "" "C:\Program Files\Google\Chrome\Application\chrome_proxy.exe"  --profile-directory=Default --app-id=bjenfbepbkgiejpkopnljbdafbmbgpel"
exit
