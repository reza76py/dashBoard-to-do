@echo off
rem Opens Project Compass. Safe to run anytime: if it's already running,
rem tray.py just opens the window instead of starting a second server.
setlocal
cd /d "%~dp0"
set "PYEXE="
for /f "delims=" %%i in ('python -c "import pystray, PIL, sys; print(sys.executable)" 2^>nul') do set "PYEXE=%%i"
if not defined PYEXE for /f "delims=" %%i in ('py -3 -c "import pystray, PIL, sys; print(sys.executable)" 2^>nul') do set "PYEXE=%%i"
if not defined PYEXE (
  echo Could not find a Python with pystray and Pillow installed.
  echo Run:  python -m pip install -r requirements.txt
  pause
  exit /b 1
)
start "" "%PYEXE:python.exe=pythonw.exe%" "%~dp0tray.py"
endlocal
