@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
  start "Project Compass Server" /min py -3 server.py
) else (
  where python >nul 2>&1
  if errorlevel 1 (
    echo Python 3 is required. Install it from https://www.python.org/downloads/
    pause
    exit /b 1
  )
  start "Project Compass Server" /min python server.py
)
timeout /t 2 /nobreak >nul
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app=http://127.0.0.1:8765
) else if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
  start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app=http://127.0.0.1:8765
) else if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
  start "" "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" --app=http://127.0.0.1:8765
) else (
  start "" http://127.0.0.1:8765
)
endlocal
