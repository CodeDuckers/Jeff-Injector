@echo off
setlocal enabledelayedexpansion

set "STEAM_PATH=%ProgramFiles(x86)%\Steam"
set "GAME_FOLDER=MarvelRivals"
set "TARGET_DLLS=amd_fidelityfx_dx12.dll sl.interposer.dll sl.dlss_g.dll sl.reflex.dll QtWebEngineProcess.exe"
set "INSTALL_PATH="

rem Add default library
set "LIBRARY_PATHS=%STEAM_PATH%\steamapps"

rem Parse additional libraries from libraryfolders.vdf
for /f "tokens=2 delims== " %%G in ('findstr /R /C:"^\s*""[0-9]""\s*""[^""]\+""" "%STEAM_PATH%\steamapps\libraryfolders.vdf"') do (
    set "LIB_PATH=%%~G"
    set "LIB_PATH=!LIB_PATH:\=\\!"
    set "LIB_PATH=!LIB_PATH:~1,-1!"
    set "LIBRARY_PATHS=!LIBRARY_PATHS!;!LIB_PATH!\steamapps"
)

rem Search for MarvelRivals in all libraries
for %%L in (!LIBRARY_PATHS!) do (
    if exist "%%L\common\%GAME_FOLDER%" (
        set "INSTALL_PATH=%%L\common\%GAME_FOLDER%"
        goto :found
    )
)

:found
if not defined INSTALL_PATH (
    echo Could not find %GAME_FOLDER% in any Steam library.
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
