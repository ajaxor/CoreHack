@echo off
echo NetHack Build Helper
echo ===================
echo.

cd /d "%~dp0"

if not exist "sys\windows\vs\NetHack.sln" (
    echo Error: NetHack.sln not found in sys\windows\vs directory.
    echo This script must be run from the NetHack root directory.
    exit /b 1
)

echo Starting build process...
echo.
cd sys\windows\vs
call build.bat
if errorlevel 1 (
    echo Build failed. See error messages above.
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo To run NetHack:
echo - Debug builds: sys\windows\vs\Debug\NetHackW.exe (GUI) or NetHack.exe (Console)
echo - Release builds: sys\windows\vs\Release\NetHackW.exe (GUI) or NetHack.exe (Console)
echo.
echo You can also find x64 builds in the x64\Debug and x64\Release directories.

cd /d "%~dp0"
