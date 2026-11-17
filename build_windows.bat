@echo off
setlocal
cd /d "%~dp0"
title Building AKIRA NIHONGO - Windows executable

echo.
echo   AKIRA NIHONGO - Windows build
echo   ----------------------------------------
echo.

python -m PyInstaller --noconfirm --clean akira_nihongo.spec
if errorlevel 1 goto failed

if not exist "dist\AkiraNihongo.exe" goto failed

echo.
echo   SUCCESS: dist\AkiraNihongo.exe
echo   ----------------------------------------
echo.
exit /b 0

:failed
echo.
echo   BUILD FAILED - see the log above.
echo.
exit /b 1
