@echo off
setlocal enabledelayedexpansion

if "%1"=="--quiet" (
    set QUIET_MODE=1
) else (
    set QUIET_MODE=0
    echo NetHack Build Script
    echo ===================
)

rem Check if Lua source files exist
if not exist "..\..\..\..\lib\lua-5.4.6\src\lapi.c" (
    echo ERROR: Lua source files not found.
    echo Expected path: ..\..\..\..\lib\lua-5.4.6\src\lapi.c
    echo Current directory: %CD%
    echo.
    echo Please make sure:
    echo 1. You have downloaded the Lua 5.4.6 source code
    echo 2. It is placed in the correct location (lib\lua-5.4.6)
    echo 3. You are running this script from sys\windows\vs directory
    exit /b 1
)

if "%VSCMD_VER%"=="" (
    if %QUIET_MODE%==0 echo MSBuild environment not set ... attempting to setup build environment.
    call :setup_environment
)

if "%VSCMD_VER%"=="" (
    echo Unable to setup build environment. Exiting.
    exit /b 1
)

if %QUIET_MODE%==0 (
    echo.
    echo Building NetHack...
    echo.
)

set BUILD_CONFIGS=Debug Release
set BUILD_PLATFORMS=x64

for %%c in (%BUILD_CONFIGS%) do (
    for %%p in (%BUILD_PLATFORMS%) do (
        if %QUIET_MODE%==0 echo Building %%c for %%p...
        msbuild NetHack.sln /t:Clean;Build /p:Configuration=%%c;Platform=%%p /nologo /verbosity:minimal
        if errorlevel 1 (
            if %QUIET_MODE%==0 (
                echo.
                echo Build failed for %%c/%%p configuration
                echo If you're seeing errors about missing Lua files, make sure:
                echo 1. You have downloaded the Lua 5.4.6 source code
                echo 2. It is placed in the correct location (lib\lua-5.4.6)
                echo 3. You are running this script from sys\windows\vs directory
            )
            exit /b 1
        )
        if %QUIET_MODE%==0 (
            echo %%c/%%p build completed successfully
            echo.
        )
    )
)

if %QUIET_MODE%==0 echo All builds completed successfully!
goto :EOF

:setup_environment
cd %~dp0
echo Searching for Visual Studio installation...

rem Try Visual Studio 2022 (VS170)
call :try_vs_version 2022 17.0 VS170COMNTOOLS
if "%VSCMD_VER%"=="" call :try_vs_version 2019 16.0 VS160COMNTOOLS
if "%VSCMD_VER%"=="" call :try_vs_version 2017 15.0 VS150COMNTOOLS

if "%VSCMD_VER%"=="" (
    echo Cannot find Visual Studio 2017, 2019, or 2022 installation.
    echo Please make sure Visual Studio is installed with C++ development tools.
    echo You can also run this script from a Visual Studio Developer Command Prompt.
)

cd %~dp0
goto :EOF

:try_vs_version
echo Checking for Visual Studio %1...
set VS_VERSION=%1
set VS_VER_NUM=%2
set VS_COMNTOOLS_VAR=%3

rem Check for VS Professional
if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\%VS_VERSION%\Professional\Common7\Tools" (
    set "%VS_COMNTOOLS_VAR%=%ProgramFiles(x86)%\Microsoft Visual Studio\%VS_VERSION%\Professional\Common7\Tools\"
    goto :run_vscmd
)

rem Check for VS Enterprise
if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\%VS_VERSION%\Enterprise\Common7\Tools" (
    set "%VS_COMNTOOLS_VAR%=%ProgramFiles(x86)%\Microsoft Visual Studio\%VS_VERSION%\Enterprise\Common7\Tools\"
    goto :run_vscmd
)

rem Check for VS Community
if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\%VS_VERSION%\Community\Common7\Tools" (
    set "%VS_COMNTOOLS_VAR%=%ProgramFiles(x86)%\Microsoft Visual Studio\%VS_VERSION%\Community\Common7\Tools\"
    goto :run_vscmd
)

rem Check for VS2022+ new path format
if exist "%ProgramFiles%\Microsoft Visual Studio\%VS_VERSION%\Professional\Common7\Tools" (
    set "%VS_COMNTOOLS_VAR%=%ProgramFiles%\Microsoft Visual Studio\%VS_VERSION%\Professional\Common7\Tools\"
    goto :run_vscmd
)
if exist "%ProgramFiles%\Microsoft Visual Studio\%VS_VERSION%\Enterprise\Common7\Tools" (
    set "%VS_COMNTOOLS_VAR%=%ProgramFiles%\Microsoft Visual Studio\%VS_VERSION%\Enterprise\Common7\Tools\"
    goto :run_vscmd
)
if exist "%ProgramFiles%\Microsoft Visual Studio\%VS_VERSION%\Community\Common7\Tools" (
    set "%VS_COMNTOOLS_VAR%=%ProgramFiles%\Microsoft Visual Studio\%VS_VERSION%\Community\Common7\Tools\"
    goto :run_vscmd
)

goto :EOF

:run_vscmd
echo Found Visual Studio %VS_VERSION%
if exist "!%VS_COMNTOOLS_VAR%!VsMSBuildCmd.bat" (
    call "!%VS_COMNTOOLS_VAR%!VsMSBuildCmd.bat"
) else if exist "!%VS_COMNTOOLS_VAR%!VsDevCmd.bat" (
    call "!%VS_COMNTOOLS_VAR%!VsDevCmd.bat"
)
echo Visual Studio %VS_VERSION% environment initialized
goto :EOF
