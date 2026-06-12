@echo off
echo Starting MindGuard Server...
call venv\Scripts\activate.bat
uvicorn main:app --host 0.0.0.0 --reload
pause
