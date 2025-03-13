@echo off
setlocal enabledelayedexpansion

echo NetHack Build Script
echo ===================

if "%VSCMD_VER%"=="" (
	echo MSBuild environment not set ... attempting to setup build environment.
	call :setup_environment
)

if "%VSCMD_VER%"=="" (
	echo Unable to setup build environment. Exiting.
	goto :EOF
)

echo.
echo Building NetHack...
echo.

set BUILD_CONFIGS=Debug
set BUILD_PLATFORMS=x64

for %%c in (%BUILD_CONFIGS%) do (
    for %%p in (%BUILD_PLATFORMS%) do (
        echo Building %%c for %%p...
        msbuild NetHack.sln /t:Clean;Build /p:Configuration=%%c;Platform=%%p
        if errorlevel 1 (
            echo Build failed for %%c/%%p configuration
            exit /b 1
        )
        echo %%c/%%p build completed successfully
        echo.
    )
)

echo All builds completed successfully!
goto :EOF

:setup_environment
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
