@echo off
setlocal enabledelayedexpansion

:: Configure output directory via environment variable with a default fallback
if "%HELPERS_DIR%"=="" set "HELPERS_DIR=scripts\helpers"
if not exist "%HELPERS_DIR%" mkdir "%HELPERS_DIR%"

:: Detect CPU architecture
set "ARCH="
if /i "%PROCESSOR_ARCHITECTURE%"=="AMD64" set "ARCH=x64"
if /i "%PROCESSOR_ARCHITECTURE%"=="ARM64" set "ARCH=arm64"
if /i "%PROCESSOR_ARCHITEW6432%"=="AMD64" set "ARCH=x64"
if /i "%PROCESSOR_ARCHITEW6432%"=="ARM64" set "ARCH=arm64"

if "%ARCH%"=="" (
    echo [ERROR] Unsupported CPU architecture: %PROCESSOR_ARCHITECTURE% >&2
    exit /b 1
)

:: Check for .NET 10 runtime availability
set "HAS_DOTNET10=0"
where dotnet >nul 2>nul
if %errorlevel% EQU 0 (
    dotnet --list-runtimes 2>nul | findstr /C:"Microsoft.NETCore.App 10." >nul
    if !errorlevel! EQU 0 (
        set "HAS_DOTNET10=1"
    )
)

if "!HAS_DOTNET10!"=="1" (
    echo [.NET 10 Found] Target: framework-dependent binaries
) else (
    echo [.NET 10 Not Found] Target: self-contained binaries
)

echo Destination directory: %HELPERS_DIR%

:: Download BACAP Addon Helper
call :DownloadAsset "ItzSkyReed/BACAP-Addon-Helper" "BACAP_Addon_Helper" "bacap_addon_helper.exe"
if !errorlevel! NEQ 0 exit /b 1

:: Download WB Addon Helper
call :DownloadAsset "ItzSkyReed/WB-Addon-Helper" "WB_Addon_Helper" "wb_addon_helper.exe"
if !errorlevel! NEQ 0 exit /b 1

echo [SUCCESS] All helpers downloaded and ready in %HELPERS_DIR%.
exit /b 0

:: ============================================================================
:: Function: DownloadAsset
:: Description:
::   Downloads the appropriate binary release asset from GitHub into HELPERS_DIR.
::
:: Arguments:
::   %~1 - Repository slug (e.g. "ItzSkyReed/BACAP-Addon-Helper")
::   %~2 - Asset prefix (e.g. "BACAP_Addon_Helper")
::   %~3 - Executable base filename (e.g. "bacap_addon_helper.exe")
::
:: Returns:
::   0 on success, 1 on failure.
::
:: Example:
::   call :DownloadAsset "ItzSkyReed/WB-Addon-Helper" "WB_Addon_Helper" "wb_addon_helper.exe"
:: ============================================================================
:DownloadAsset
set "REPO=%~1"
set "PREFIX=%~2"
set "TARGET_NAME=%~3"
set "TARGET_PATH=%HELPERS_DIR%\%TARGET_NAME%"

if "!HAS_DOTNET10!"=="1" (
    set "ASSET=!PREFIX!-framework-dependent-win-%ARCH%.exe"
) else (
    set "ASSET=!PREFIX!-win-%ARCH%.exe"
)

set "URL=https://github.com/!REPO!/releases/latest/download/!ASSET!"
echo Fetching !ASSET! -> !TARGET_PATH!...

where curl.exe >nul 2>nul
if %errorlevel% EQU 0 (
    curl.exe -f -L "!URL!" -o "!TARGET_PATH!"
) else (
    powershell -NoProfile -Command "$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri '!URL!' -OutFile '!TARGET_PATH!'"
)

if %errorlevel% NEQ 0 (
    echo [ERROR] Failed to download !TARGET_PATH!. >&2
    if exist "!TARGET_PATH!" del "!TARGET_PATH!"
    exit /b 1
)

echo [OK] Saved !TARGET_PATH!
exit /b 0