@echo off
title Kiris Hesaplayici - Sunucu

echo.
echo  ====================================
echo   Kiris Hesaplayici  v1.0
echo  ====================================
echo.

:: Python kontrolu
echo [1/4] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [HATA] Python bulunamadi!
    echo  Lutfen https://www.python.org/downloads/
    echo  adresinden Python 3.10+ indirin.
    echo  Kurulumda "Add Python to PATH" secin.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  [OK] %PYVER%
echo.

:: pip guncelle
echo [2/4] pip guncelleniyor...
python -m pip install --upgrade pip --quiet
echo  [OK] pip hazir.
echo.

:: Bagimliliklar
echo [3/4] Bagimliliklar yukleniyor...
echo  fastapi, uvicorn, numpy, pydantic
echo.
python -m pip install fastapi "uvicorn[standard]" numpy "pydantic>=2.7.0" python-multipart --quiet
if errorlevel 1 (
    echo.
    echo  [HATA] Paket yukleme basarisiz!
    echo  Internet baglantinizi kontrol edin.
    echo.
    pause
    exit /b 1
)
echo  [OK] Bagimliliklar yuklendi.
echo.

:: projects klasoru
if not exist "projects" mkdir projects

:: Sunucuyu baslat
echo [4/4] Sunucu baslatiliyor...
echo.
echo  ====================================
echo   Uygulama : http://localhost:8000
echo   API Docs : http://localhost:8000/docs
echo   Durdurmak icin: Ctrl+C
echo  ====================================
echo.

start "" http://localhost:8000
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --no-use-colors

echo.
echo  Sunucu kapatildi.
pause
