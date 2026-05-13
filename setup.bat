@echo off
rem Setup script for Icaron IHA OpenCV environment

rem Change to script directory
cd /d "%~dp0"

rem Create virtual environment if not exists
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

rem Activate virtual environment
call venv\Scripts\activate.bat

rem Upgrade pip
python -m pip install --upgrade pip

rem Install required packages
pip install -r requirements.txt

echo Setup complete. Use "venv\Scripts\activate.bat" to activate the environment.
pause
