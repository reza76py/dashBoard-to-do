@echo off
setlocal
set "APPBAT=%~dp0start_windows.bat"
set "AUTOSTART=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Project Compass.lnk"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$sh=New-Object -ComObject WScript.Shell; $link=$sh.CreateShortcut($env:AUTOSTART); $link.TargetPath=$env:APPBAT; $link.WorkingDirectory=(Split-Path $env:APPBAT); $link.Description='Start Project Compass on sign in'; $link.Save()"
if %errorlevel% neq 0 (
  echo Could not create the startup shortcut.
) else (
  echo Project Compass will open when you sign in to Windows.
  echo To disable, remove 'Project Compass' from the Startup folder: Win+R ^> shell:startup
)
pause
endlocal
