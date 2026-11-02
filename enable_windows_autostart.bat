@echo off
setlocal
cd /d "%~dp0"
set "TRAY=%~dp0tray.py"
set "AUTOSTART=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Project Compass.lnk"
rem Use the first Python that has the tray packages installed (pip install -r requirements.txt).
set "PYEXE="
for /f "delims=" %%i in ('python -c "import pystray, PIL, sys; print(sys.executable)" 2^>nul') do set "PYEXE=%%i"
if not defined PYEXE for /f "delims=" %%i in ('py -3 -c "import pystray, PIL, sys; print(sys.executable)" 2^>nul') do set "PYEXE=%%i"
if not defined PYEXE (
  echo Could not find a Python with pystray and Pillow installed.
  echo Run:  python -m pip install -r requirements.txt
  pause
  exit /b 1
)
set "PYW=%PYEXE:python.exe=pythonw.exe%"
set "TRAYARG="%TRAY%""
powershell -NoProfile -ExecutionPolicy Bypass -Command "$sh=New-Object -ComObject WScript.Shell; $link=$sh.CreateShortcut($env:AUTOSTART); $link.TargetPath=$env:PYW; $link.Arguments=$env:TRAYARG; $link.WorkingDirectory=(Split-Path $env:TRAY); $link.Description='Start Project Compass tray on sign in'; $link.Save()"
if errorlevel 1 (
  echo Could not create the startup shortcut.
) else (
  echo Project Compass tray will start when you sign in to Windows.
  echo Python: %PYW%
  echo To disable, remove 'Project Compass' from the Startup folder: Win+R ^> shell:startup
)
pause
endlocal
