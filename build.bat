@echo off
title BUILD BARA PRANK EXE
color 0C
cd /d "%~dp0"

echo.
echo   ============================================
echo    BUILD BARA PRANK.EXE
echo    Created by BARA
echo   ============================================
echo.

echo [*] Install dependensi...
pip install colorama pywin32 pyinstaller

echo [*] Build .exe...
pyinstaller --onefile --noconsole --name "bara-prank" main.py

echo.
echo   ============================================
echo    [OK] BUILD SELESAI
echo    File: dist\bara-prank.exe
echo   ============================================
echo.

pause
