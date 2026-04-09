@echo off
cd /d "%~dp0"
echo ============================================
echo  SQL Query Practice - Windows Setup
echo ============================================
echo.

:: ── Step 1: Find or install Python ──────────────────────────────────────────
set PYTHON=
where py >nul 2>&1
if not errorlevel 1 set PYTHON=py

if "%PYTHON%"=="" (
    where python >nul 2>&1
    if not errorlevel 1 (
        :: Verify it's not the Microsoft Store stub (stub outputs "Python" with no version)
        for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
        if not "%PY_VER%"=="" set PYTHON=python
    )
)

if "%PYTHON%"=="" (
    where python3 >nul 2>&1
    if not errorlevel 1 (
        for /f "tokens=2" %%v in ('python3 --version 2^>^&1') do set PY_VER=%%v
        if not "%PY_VER%"=="" set PYTHON=python3
    )
)

if not "%PYTHON%"=="" goto :python_found

:: Python not found - try winget
echo Python not found. Attempting automatic installation...
echo.
where winget >nul 2>&1
if errorlevel 1 goto :try_powershell

echo Installing Python via winget...
winget install --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"
where py >nul 2>&1
if not errorlevel 1 set PYTHON=py
if not "%PYTHON%"=="" goto :python_found

:try_powershell
echo Downloading Python 3.11 installer...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\python_installer.exe'"
if errorlevel 1 goto :python_fail

echo Running Python installer...
"%TEMP%\python_installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1
del "%TEMP%\python_installer.exe" >nul 2>&1
set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"
where py >nul 2>&1
if not errorlevel 1 set PYTHON=py
where python >nul 2>&1
if not errorlevel 1 set PYTHON=python
if not "%PYTHON%"=="" goto :python_found

:python_fail
echo ERROR: Python not found and could not be installed automatically.
echo Please install Python manually from https://python.org
echo Make sure to check "Add Python to PATH" during installation.
pause
exit /b 1

:python_found
echo Python found: %PYTHON%
%PYTHON% --version
echo.

:: ── Step 2: Create virtual environment ──────────────────────────────────────
if exist "venv\Scripts\activate.bat" goto :venv_ok

echo Creating virtual environment...
if exist "venv" rmdir /s /q venv
%PYTHON% -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

:venv_ok
call venv\Scripts\activate.bat
echo Virtual environment activated.
echo.

:: ── Step 3: Install dependencies ────────────────────────────────────────────
echo Installing dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo Dependencies installed.
echo.

:: ── Step 4: Find a free port starting from 5000 ─────────────────────────────
setlocal enabledelayedexpansion
set PORT=5000

:find_port
powershell -Command "$c=New-Object Net.Sockets.TcpClient;try{$c.Connect('127.0.0.1',!PORT!);$c.Close();exit 1}catch{exit 0}" >nul 2>&1
if errorlevel 1 (
    set /a PORT=!PORT!+1
    goto :find_port
)

:: ── Step 5: Start the app ────────────────────────────────────────────────────
echo ============================================
echo  Starting at http://localhost:!PORT!
echo  Press Ctrl+C to stop
echo ============================================
echo.

start /b powershell -Command "Start-Sleep -Milliseconds 2000; Start-Process 'http://localhost:!PORT!'"

set PORT=!PORT!
python app.py
