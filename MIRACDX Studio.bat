@echo off
title MIRACDX Studio
cd /d "%~dp0"
echo Starting MIRACDX Studio...
start "" pythonw "%~dp0studio\server.py"
timeout /t 2 >nul
start "" "http://127.0.0.1:7799/studio/studio.html"
echo.
echo MIRACDX Studio is running in your browser.
echo Server: http://127.0.0.1:7799
echo Close this window (and the studio tab) when done.
echo To fully stop the server, open Task Manager and end "pythonw.exe".
echo.
pause
