@echo off
setlocal

set taskname=RunD2PTUpdateService
set scriptpath=%~dp0main.py

schtasks /delete /tn %taskname% /f >nul 2>&1
schtasks /Create /TN %taskname% /TR "pythonw %scriptpath%" /SC HOURLY /F

if %errorlevel% equ 0 (
    echo Task "%taskname%" created successfully.
) else (
    echo Failed to create task "%taskname%".
    exit /b %errorlevel%
)

schtasks /Run /TN %taskname%
endlocal
pause