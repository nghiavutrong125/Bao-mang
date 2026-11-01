@echo off
chcp 65001 > nul
title XU LY ANH & DONG BO R2 - FIFTY FIFTY MAGAZINE

echo =======================================================
echo     HE THONG XU LY ANH & DONG BO CLOUDFLARE R2
echo              FIFTY FIFTY MAGAZINE
echo =======================================================
echo.

set /p NAME=">> Nhap ten goc SEO cho anh (VD: ha-giang-loop, hanoi-food): "
if "%NAME%"=="" (
    echo [LOI] Ban chua nhap ten anh!
    pause
    exit /b
)

echo.
echo Chon ty le anh:
echo [1] 16:9 (Hero banner, anh dau bai viet - 1200x675)
echo [2] 3:2  (The card tieu chuan - 1200x800)
echo [3] max  (Giu nguyen ty le goc, toi da 1600px) [Mac dinh]
set /p ASPECT_CHOICE=">> Chon ty le (1/2/3): "

set ASPECT=max
if "%ASPECT_CHOICE%"=="1" set ASPECT=16:9
if "%ASPECT_CHOICE%"=="2" set ASPECT=3:2

echo.
echo Dang xu ly anh tu thu muc photos-raw...
python tools\image_pipeline.py --input photos-raw --name "%NAME%" --aspect %ASPECT%

echo.
pause
