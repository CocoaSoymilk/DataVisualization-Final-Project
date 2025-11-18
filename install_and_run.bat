@echo off
chcp 65001 > nul
echo ================================
echo   패키지 설치 및 대시보드 실행
echo ================================
echo.

echo [1/2] requests 패키지 설치 중...
pip install requests==2.31.0
echo.

echo [2/2] 대시보드 시작 중...
echo.
python app.py

