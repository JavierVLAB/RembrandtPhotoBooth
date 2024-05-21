@echo off
cd C:\Users\User\RembrandtPhotoBooth\backend
call venv\Scripts\activate
uvicorn main:app --reload
