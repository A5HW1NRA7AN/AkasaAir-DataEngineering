@echo off
REM ==========================================================
REM Akasa Air - Daily ETL Runner + Scheduler
REM This script:
REM 1) runs the ETL once
REM 2) creates a Windows Scheduled Task to run daily at 9:00 AM
REM ----------------------------------------------------------
REM IMPORTANT: update PROJECT_PATH below to your actual folder
REM ==========================================================

REM ---- 0. CONFIGURE THESE PATHS ----
set "PROJECT_PATH=C:\Users\rajan\OneDrive\Desktop\College\Placement\Assesement\Akasa\AkasaAir-DataEngineering"
set "VENV_PATH=%PROJECT_PATH%\.venv\Scripts\activate"
set "PYTHON_SCRIPT=%PROJECT_PATH%\run_pipeline.py"
set "TASK_NAME=AkasaAir_Daily_ETL"
REM time in 24-hr format
set "TASK_TIME=09:00"

REM ---- 1. RUN THE ETL ONCE NOW ----
echo.
echo [INFO] Running ETL once now...
cd /d "%PROJECT_PATH%"

call "%VENV_PATH%"
python "%PYTHON_SCRIPT%"
REM optional: deactivate
call deactivate 2>nul

echo [INFO] ETL run finished.
echo.

REM ---- 2. CREATE / UPDATE SCHEDULED TASK ----
echo [INFO] Creating or updating Windows scheduled task: %TASK_NAME%
echo [INFO] It will run daily at %TASK_TIME%

REM We call cmd.exe to run our batch every day.
REM /SC DAILY  -> daily
REM /ST 09:00  -> at 9 AM
REM /RL HIGHEST -> run with highest privileges
REM /F -> force update if task exists

schtasks /Create ^
 /TN "%TASK_NAME%" ^
 /TR "\"%PROJECT_PATH%\setup_and_run_etl.bat\"" ^
 /SC DAILY ^
 /ST %TASK_TIME% ^
 /RL HIGHEST ^
 /F

IF %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Task %TASK_NAME% created/updated to run daily at %TASK_TIME%.
) ELSE (
    echo [ERROR] Failed to create scheduled task. Try running this .bat as Administrator.
)

echo.
echo [DONE] You can close this window now.
pause
