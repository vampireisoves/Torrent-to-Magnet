@echo off
chcp 65001 >nul
echo ==============================================
echo          一键打包 GUI 程序
echo ==============================================
echo.

python -m PyInstaller -F -w --name=BT文件转磁力链 torrent_to_magnet_gui.py

echo.
echo ✅ 打包完成！EXE 文件在 dist 文件夹里
echo.
pause