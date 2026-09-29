@echo off
title BARA HACK TOOL
color 0C
cd /d "%~dp0"

reg add "HKCU\Console" /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

python main.py
pause
