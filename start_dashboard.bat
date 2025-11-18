@echo off
chcp 65001 > nul
cd /d "C:\Users\tree1\Desktop\교통사고 대시보드"
echo ========================================
echo Starting Dashboard...
echo ========================================
python app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Dashboard failed to start!
    pause
)
