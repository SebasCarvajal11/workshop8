@echo off
cd /d "%~dp0.."
if not exist ".venv\Scripts\activate.bat" (
  echo Falta el entorno virtual. Ejecute primero iniciar.bat en la raiz del proyecto.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
echo API FastAPI + CLIPS en http://127.0.0.1:8000
echo Cierre esta ventana para detener la API.
pricing-api
pause
