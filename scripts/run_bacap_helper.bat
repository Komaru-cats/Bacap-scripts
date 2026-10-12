@echo off
setlocal enabledelayedexpansion

:: Load .env.bacap_addon from working directory if it exists
if exist ".env.bacap_addon" (
    for /f "usebackq eol=# tokens=1* delims==" %%A in (".env.bacap_addon") do (
        set "%%A=%%B"
    )
)

:: Execute the helper binary with all passed arguments
"%~dp0helpers\bacap_addon_helper.exe" %*