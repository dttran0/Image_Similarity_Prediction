@echo off
setlocal

REM Set paths to Conda and VSCode installers
set CONDA_INSTALL_PATH=%USERPROFILE%\Miniconda3
set VENV_NAME=rages
set REQUIREMENTS_FILE=requirements.txt

REM Create virtual environment
echo Creating virtual environment...
call conda create -y -n %VENV_NAME% python=3.12

REM Activate virtual environment
echo Activating virtual environment...
call conda activate %VENV_NAME%
python --version
REM install package from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r %REQUIREMENTS_FILE%

endlocal
pause
