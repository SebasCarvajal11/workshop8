@echo off
setlocal EnableExtensions
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo === El Mercantil / Workshop precios dinamicos ===
echo Instalacion y arranque (Python + Node.js)
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] No se encontro "python" en PATH. Instale Python 3.11 o superior.
  goto :fail
)

python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Se requiere Python 3.11 o superior.
  python --version
  goto :fail
)

where node >nul 2>&1
if errorlevel 1 (
  echo [ERROR] No se encontro "node" en PATH. Instale Node.js 18 o superior.
  goto :fail
)

call :ensure_pnpm
if errorlevel 1 goto :fail

echo [1/4] Entorno virtual Python...
if not exist ".venv\Scripts\python.exe" (
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] No se pudo crear .venv
    goto :fail
  )
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip -q
echo [2/4] Paquete pricing-expert (CLIPS + API)...
pip install -e .
if errorlevel 1 (
  echo [ERROR] pip install -e . fallo
  goto :fail
)

echo [3/4] Dependencias web (pnpm)...
cd /d "%~dp0web"
call pnpm install
if errorlevel 1 (
  echo [ERROR] pnpm install fallo. Revise web\pnpm-workspace.yaml (esbuild: true^).
  cd /d "%~dp0"
  goto :fail
)
cd /d "%~dp0"

echo [4/4] Iniciando servidores...
start "Pricing API :8000" cmd /k "%~dp0scripts\run-dev-api.bat"
timeout /t 2 /nobreak >nul
start "El Mercantil :5173" cmd /k "%~dp0scripts\run-dev-web.bat"
timeout /t 2 /nobreak >nul
start "" http://localhost:5173/

echo.
echo Listo.
echo   Web:  http://localhost:5173
echo   API:  http://127.0.0.1:8000
echo.
echo Dos ventanas CMD quedaron abiertas (API y Vite^). Cierrelas para detener.
echo.
pause
exit /b 0

:ensure_pnpm
where pnpm >nul 2>&1
if not errorlevel 1 exit /b 0
echo pnpm no esta en PATH; activando con Corepack (incluido en Node.js^)...
where corepack >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Instale Node.js reciente o instale pnpm: https://pnpm.io/installation
  exit /b 1
)
call corepack enable
call corepack prepare pnpm@11.1.1 --activate
where pnpm >nul 2>&1
if errorlevel 1 (
  echo [ERROR] No se pudo activar pnpm.
  exit /b 1
)
exit /b 0

:fail
echo.
pause
exit /b 1
