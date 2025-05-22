@echo off
setlocal enabledelayedexpansion

set "STEAM_PATH=%ProgramFiles(x86)%\Steam"
set "APP_ID=2767030"
set "TARGET_DLLS=amd_fidelityfx_dx12.dll sl.interposer.dll sl.dlss_g.dll sl.reflex.dll"
set "INSTALL_PATH="

rem Check default library
if exist "%STEAM_PATH%\steamapps\appmanifest_%APP_ID%.acf" (
    for /f "tokens=2 delims=\" %%A in ('findstr /i /c:"installdir" "%STEAM_PATH%\steamapps\appmanifest_%APP_ID%.acf"') do (
        set "INSTALL_PATH=%STEAM_PATH%\steamapps\common\%%A"
    )
)

rem Check additional libraries from libraryfolders.vdf
if not defined INSTALL_PATH (
    for /f "tokens=2 delims== " %%G in ('findstr /R /C:"^\s*""[0-9]""\s*""[^""]\+""" "%STEAM_PATH%\steamapps\libraryfolders.vdf"') do (
        set "LIB_PATH=%%~G"
        set "LIB_PATH=!LIB_PATH:\=\\!"
        set "LIB_PATH=!LIB_PATH:~1,-1!"
        if exist "!LIB_PATH!\steamapps\appmanifest_%APP_ID%.acf" (
            for /f "tokens=2 delims=\" %%A in ('findstr /i /c:"installdir" "!LIB_PATH!\steamapps\appmanifest_%APP_ID%.acf"') do (
                set "INSTALL_PATH=!LIB_PATH!\steamapps\common\%%A"
            )
        )
    )
)

if not defined INSTALL_PATH (
    echo Could not determine install path for AppID %APP_ID%
    exit /b 1
)

echo Detected install path : %INSTALL_PATH%

rem Remove DLLs
for %%D in (%TARGET_DLLS%) do (
    for /r "%INSTALL_PATH%" %%F in (%%D) do (
        if exist "%%F" (
            echo Deleting : %%F
            del /f /q "%%F"
        )
    )
)

endlocal
