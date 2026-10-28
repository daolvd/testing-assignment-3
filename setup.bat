@echo off
setlocal enabledelayedexpansion

:: ==============================================================================
:: AUTOMATED ENVIRONMENT SETUP SCRIPT (FOR WINDOWS)
:: Automatically: creates .venv, installs requirements.txt, creates .env, and registers a test account.
:: ==============================================================================

cd /d "%~dp0"

echo ======================================================================
echo    STARTING TEST ENVIRONMENT SETUP
echo ======================================================================

:: 1. Check Python on Windows
where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% neq 0 (
        echo [ERROR] Python was not found! Please install Python 3.11+ and select "Add Python to PATH".
        pause
        exit /b 1
    ) else (
        set PY_CMD=py -3
    )
) else (
    set PY_CMD=python
)

:: 2. Automatically create the virtual environment (.venv) if it does not exist
if not exist ".venv" (
    echo [1/4] The .venv virtual environment does not exist. Creating it automatically...
    %PY_CMD% -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Could not create the .venv virtual environment!
        pause
        exit /b 1
    )
) else (
    echo [OK] The .venv virtual environment already exists.
)

:: Activate the virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [ERROR] The activate file was not found in .venv\Scripts!
    pause
    exit /b 1
)

:: 3. Automatically install dependencies
echo [2/4] Checking and installing dependencies from requirements.txt...
python -m pip install --upgrade pip >nul 2>nul
python -m pip install -r requirements.txt

:: 4. Automatically create .env from .env.example if it does not exist
if not exist ".env" (
    echo [3/4] The .env file does not exist. Creating it from .env.example...
    copy .env.example .env >nul
) else (
    echo [OK] The .env file already exists.
)

:: 5. Automatically check for and create a test account if needed
findstr /R /C:"^TEST_EMAIL=..*" .env >nul 2>nul
set EMAIL_FOUND=%errorlevel%
findstr /R /C:"^TEST_PASSWORD=..*" .env >nul 2>nul
set PWD_FOUND=%errorlevel%

if %EMAIL_FOUND% neq 0 (
    set NEED_REGISTER=1
) else if %PWD_FOUND% neq 0 (
    set NEED_REGISTER=1
) else (
    set NEED_REGISTER=0
)

if "%NEED_REGISTER%"=="1" (
    echo [4/4] Automatically registering a new test account and saving it to .env...
    python -m scripts.register_account --save-env
) else (
    echo [OK] A test account already exists in .env.
)

echo.
echo ======================================================================
echo  [SUCCESS] Setup completed successfully!
echo  Run run.bat to start testing.
echo ======================================================================
echo.

pause
exit /b 0
