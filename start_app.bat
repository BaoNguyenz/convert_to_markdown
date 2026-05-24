@echo off
title Docling Markdown Studio Launcher
echo ========================================================
echo          Docling Markdown Studio Launcher
echo ========================================================
echo.
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
    echo Make sure Anaconda/Miniconda is installed and in your PATH.
    echo.
    pause
)
