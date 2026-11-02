@echo off
setlocal
cd /d "%~dp0"
set "TRAY=%~dp0tray.py"
set "ICON=%~dp0compass.ico"
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
rem GetFolderPath('Desktop') follows OneDrive redirection; %USERPROFILE%\Desktop may not exist.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$desk=[Environment]::GetFolderPath('Desktop'); $sh=New-Object -ComObject WScript.Shell; $link=$sh.CreateShortcut((Join-Path $desk 'Project Compass.lnk')); $link.TargetPath=$env:PYW; $link.Arguments=$env:TRAYARG; $link.WorkingDirectory=(Split-Path $env:TRAY); if (Test-Path $env:ICON) { $link.IconLocation=$env:ICON }; $link.Description='Open Project Compass'; $link.Save(); Write-Host ('Shortcut created: ' + (Join-Path $desk 'Project Compass.lnk'))"
if errorlevel 1 (
  echo Could not create the desktop shortcut.
) else (
  echo Python: %PYW%
)
pause
endlocal
