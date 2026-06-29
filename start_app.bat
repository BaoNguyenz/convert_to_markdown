@echo off
setlocal enabledelayedexpansion
title Docling Markdown Studio Launcher
echo ========================================================
echo          Docling Markdown Studio Launcher
echo ========================================================
echo.

:: Detect if conda is available in current PATH
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] 'conda' command not found in PATH. Checking common installation paths...
    
    set "CONDA_FOUND=0"
    for %%D in (
        "C:\Users\VU\anaconda3"
        "%USERPROFILE%\anaconda3"
        "%USERPROFILE%\miniconda3"
        "C:\ProgramData\anaconda3"
        "C:\ProgramData\miniconda3"
    ) do (
        if exist "%%~D\Scripts\conda.exe" (
            echo [INFO] Found Conda in: %%~D
            set "PATH=%%~D;%%~D\Scripts;%%~D\Library\bin;!PATH!"
            set "CONDA_FOUND=1"
            goto CONDA_OK
        )
    )
    
    :CONDA_OK
    if "!CONDA_FOUND!"=="0" (
        echo [ERROR] Conda was not found in common locations.
        echo Please open 'Anaconda Prompt' or 'Miniconda Prompt', navigate to this folder,
        echo and run: start_app.bat
        echo.
        pause
        exit /b 1
    )
)

echo Starting FastAPI Web Server inside conda environment 'docling-env'...
echo Opening browser to http://127.0.0.1:8000 ...
echo.

:: Open browser in background after a 3 second delay
start /b cmd /c "timeout /t 3 >nul && start http://127.0.0.1:8000"

:: Execute FastAPI server using conda run
conda run -n docling-env python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server encountered an error or failed to start.
    echo.
    pause
)

