@echo off
setlocal enabledelayedexpansion

:: ==============================================================================
:: RUN ALL TESTS SCRIPT (FOR WINDOWS)
:: Automatically runs setup on the first run, then executes the Behave tests.
:: Double-click this file to run the tests.
:: ==============================================================================

cd /d "%~dp0"

:: Check whether setup is complete; if not, automatically call setup.bat
set NEEDS_SETUP=0
if not exist ".venv" set NEEDS_SETUP=1
if not exist ".env" set NEEDS_SETUP=1

if "%NEEDS_SETUP%"=="1" (
    echo [INFO] First run detected. Automatically completing the full setup...
    call setup.bat
)

:: Activate the virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [INFO] The environment is not ready. Running setup again...
    call setup.bat
    call .venv\Scripts\activate.bat
)

:: Check dependencies
python -c "import behave, selenium, dotenv" >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Dependencies are missing. Running setup again...
    call setup.bat
)

:: Check the test account
findstr /R /C:"^TEST_EMAIL=..*" .env >nul 2>nul
set EMAIL_FOUND=%errorlevel%
findstr /R /C:"^TEST_PASSWORD=..*" .env >nul 2>nul
set PWD_FOUND=%errorlevel%

if %EMAIL_FOUND% neq 0 (
    echo [INFO] Automatically registering a test account in .env...
    python -m scripts.register_account --save-env
) else if %PWD_FOUND% neq 0 (
    echo [INFO] Automatically registering a test account in .env...
    python -m scripts.register_account --save-env
)

:: Start Behave
echo ======================================================================
echo    STARTING BEHAVE TESTS...
echo ======================================================================

python -m behave %*

set BEHAVE_EXIT=%errorlevel%

echo.
echo ======================================================================
echo  [COMPLETE] Evidence and screenshots are saved at:
echo  reports\screenshots\
echo ======================================================================
echo.

pause
exit /b %BEHAVE_EXIT%
