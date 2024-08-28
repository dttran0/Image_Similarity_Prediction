@echo off
setlocal

set CONDA_INSTALL_PATH=%USERPROFILE%\Miniconda3

set VENV_NAME=rages
set PYTHON_FILE=SimilarityApp.py


REM Activate virtual environment
echo Activating virtual environment...
call conda activate %VENV_NAME%
python --version
REM Run the Python file
echo Running the Python file...
REM python %PYTHON_FILE%

REM Open VSCode
echo Opening VSCode in the current directory...
start "" code .

endlocal
pause
