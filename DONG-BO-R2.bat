@echo off
chcp 65001 > nul
title DONG BO ANH CLOUD LEN CLOUDFLARE R2

echo Dang dong bo thu muc D:\Anh_Cloud\fiftyfifty-data len Cloudflare R2 bao-mang...
"D:\My-small-app\rclone-v1.73.3-windows-amd64\rclone.exe" sync "D:\Anh_Cloud\fiftyfifty-data" "r2-baomang:bao-mang" --s3-no-check-bucket --transfers 16 --checkers 32 --fast-list -P

echo.
echo ===========================================
echo       DONG BO HOAN TAT!
echo ===========================================
pause

