@echo off
cd C:\Users\User\RembrandtPhotoBooth\backend
call venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000
