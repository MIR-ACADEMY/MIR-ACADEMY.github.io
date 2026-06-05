@echo off
title MIRACDX Studio
cd /d "%~dp0"
echo Starting MIRACDX Studio...
REM use the REAL Python in a minimized window (pythonw.exe was failing silently — engine never bound)
set "PY=C:\Users\emrem\AppData\Local\Programs\Python\Python313\python.exe"
if not exist "%PY%" set "PY=python"
start "MIRACDX Engine" /min "%PY%" "%~dp0studio\server.py"
timeout /t 3 >nul
set "BRAVE=C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
if exist "%BRAVE%" ( start "" "%BRAVE%" "http://127.0.0.1:7799/MIRACDX-Control-Center.html" ) else ( start "" "http://127.0.0.1:7799/MIRACDX-Control-Center.html" )
echo.
echo MIRACDX Studio is running in your browser.
echo Server: http://127.0.0.1:7799
echo Close this window (and the studio tab) when done.
echo To fully stop the server, open Task Manager and end "pythonw.exe".
echo.
pause
