@echo off
chcp 65001 >nul
echo ========================================
echo Torrent转Magnet工具 - 完整打包脚本
echo ========================================
echo.
echo 请选择要打包的版本:
echo   1. CLI版本 (命令行工具)
echo   2. GUI版本 (图形界面)
echo   3. 两个版本都打包
echo.
set /p choice="请输入选项 (1/2/3): "

if "%choice%"=="1" goto build_cli
if "%choice%"=="2" goto build_gui
if "%choice%"=="3" goto build_all
echo 无效选项
pause
exit /b 1

:build_cli
echo.
echo ========================================
echo 开始打包CLI版本...
echo ========================================
call build_cli.bat
goto end

:build_gui
echo.
echo ========================================
echo 开始打包GUI版本...
echo ========================================
call build_gui.bat
goto end

:build_all
echo.
echo ========================================
echo 开始打包CLI版本...
echo ========================================
call build_cli.bat
echo.
echo ========================================
echo 开始打包GUI版本...
echo ========================================
call build_gui.bat
goto end

:end
echo.
echo ========================================
echo 所有打包任务完成！
echo ========================================
echo.
echo 文件位置:
if exist dist\TorrentToMagnet.exe echo   CLI版本: dist\TorrentToMagnet.exe
if exist dist\TorrentToMagnet_GUI.exe echo   GUI版本: dist\TorrentToMagnet_GUI.exe
echo.
pause