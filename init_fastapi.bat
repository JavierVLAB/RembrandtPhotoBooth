@echo off
cd C:\ruta\de\tu\proyecto\fastapi
python -m venv venv
call venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000
