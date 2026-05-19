@echo off
REM Ajuste CLIPS_EXECUTABLE si clips.exe no está en PATH
set CLIPS_EXE=clips
cd /d "%~dp0..\clips"
echo Cargue manualmente en CLIPS: (load "pricing-rules.clp") luego un escenario en scenarios\
%CLIPS_EXE%
