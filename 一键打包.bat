@echo off
chcp 65001 >nul
echo ==============================================
echo          一键打包 GUI 程序（无黑窗口）
echo ==============================================
echo.

python -m PyInstaller -F -w torrent_to_magnet_gui.py

echo.
echo ✅ 打包完成！EXE 文件在 dist 文件夹里
echo.
pause