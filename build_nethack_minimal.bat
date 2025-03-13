@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

if not exist "sys\windows\vs\NetHack.sln" (
    echo ERROR: NetHack.sln not found in sys\windows\vs directory.
    exit /b 1
)

cd sys\windows\vs

rem Capture build output to a temporary file
set "temp_log=%TEMP%\nethack_build_log.txt"
call build.bat > "%temp_log%" 2>&1
set build_result=%errorlevel%

if %build_result% neq 0 (
    echo BUILD FAILED with exit code %build_result%
    
    rem Display only error lines from the log (limited to 10)
    echo Showing up to 10 error messages:
    findstr /i /C:"error" "%temp_log%" | findstr /v /i /C:"0 error(s)" | findstr /v /i /C:"with 0 error" > "%temp_log%_errors.txt"
    set error_count=0
    for /f "tokens=*" %%a in ('type "%temp_log%_errors.txt"') do (
        set /a error_count+=1
        if !error_count! leq 10 echo %%a
    )
    if !error_count! gtr 10 echo ... (additional errors not shown)
    
    del "%temp_log%" "%temp_log%_errors.txt" 2>nul
    exit /b 1
) else (
    echo BUILD SUCCESSFUL
    del "%temp_log%" 2>nul
    exit /b 0
)
