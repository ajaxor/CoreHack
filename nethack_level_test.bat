@echo off
setlocal enabledelayedexpansion

REM NetHack Level Test Script
REM Tests level generation using NetHack's test mode (-t)
REM Returns success (0) if test passes, error code otherwise

echo NetHack Level Test Script
echo ========================

cd binary\Debug\x64\
REM Find NetHack executable
set "NETHACK_EXE=.\NetHack.exe"
if not exist "%NETHACK_EXE%" (
    set "NETHACK_EXE=.\nethack.exe"
)
if not exist "%NETHACK_EXE%" (
    set "NETHACK_EXE=.\build\nethack.exe"
)
if not exist "%NETHACK_EXE%" (
    echo ERROR: Could not find NetHack executable.
    echo Please run this script from the NetHack source directory.
    exit /b 1
)

echo Using NetHack executable: %NETHACK_EXE%

REM Determine paniclog location
set "PANICLOG=%USERPROFILE%\NetHack\3.7\paniclog"
if not exist "%USERPROFILE%\NetHack\3.7\" (
    echo WARNING: Default paniclog location not found.
    echo Checking current directory...
    if exist "paniclog" (
        set "PANICLOG=paniclog"
    ) else (
        echo ERROR: Could not find paniclog location.
        echo Please specify the path to the paniclog in the script.
        exit /b 1
    )
)

echo Using paniclog: %PANICLOG%

REM Clear the paniclog
echo Clearing paniclog...
if exist "%PANICLOG%" (
    del "%PANICLOG%"
)

REM Get level to test from command line or use default
set LEVEL=4
if not "%~1"=="" set LEVEL=%~1

echo Testing level %LEVEL% generation...

REM Run NetHack in test mode
"%NETHACK_EXE%" -t %LEVEL%

REM Check if paniclog exists
if not exist "%PANICLOG%" (
    echo ERROR: Nethack crashed while loading Level %LEVEL% 
    exit /b 1
)

echo.
echo Paniclog contents:
echo -----------------
type "%PANICLOG%"
echo -----------------
echo.

REM Check for success message in paniclog
findstr /C:"Test Successful" "%PANICLOG%" > nul
if %ERRORLEVEL% equ 0 (
    REM Count lines in paniclog
    for /f %%A in ('type "%PANICLOG%" ^| find /c /v ""') do set "LINECOUNT=%%A"
    
    if !LINECOUNT! equ 1 (
        echo TEST PASSED: Level %LEVEL% generation successful.
        exit /b 0
    ) else (
        echo TEST FAILED: See log
        exit /b 1
    )
) else (
    echo TEST FAILED: See log
    exit /b 1
)
