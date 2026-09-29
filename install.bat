@echo off
title BARA HACK TOOL - INSTALLER
color 0C
cd /d "%~dp0"

echo.
echo   ============================================
echo    BARA HACK TOOL - INSTALLER
echo    Created by BARA
echo   ============================================
echo.

echo [*] Cek Python...
python --version
if errorlevel 1 (
    echo [!] Python tidak ditemukan. Install dulu dari python.org
    pause
    exit /b
)

echo [*] Install dependensi...
pip install colorama pywin32 pyinstaller

echo.
echo   ============================================
echo    [OK] INSTALL SELESAI
echo    Jalankan: python main.py atau run.bat
echo   ============================================
echo.

pause
