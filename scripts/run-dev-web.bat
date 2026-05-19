@echo off
cd /d "%~dp0..\web"
if not exist "node_modules" (
  echo Falta node_modules. Ejecute primero iniciar.bat en la raiz del proyecto.
  pause
  exit /b 1
)
echo Tienda Vite en http://localhost:5173
echo Cierre esta ventana para detener el frontend.
pnpm dev
pause
