@echo off
chcp 65001 >nul
echo ========================================
echo Torrent转Magnet工具 - GUI版打包脚本
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

:: 检查pip是否可用
pip --version >nul 2>&1
if errorlevel 1 (
    echo 错误: pip不可用
    pause
    exit /b 1
)

echo [1/4] 安装依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

echo.
echo [2/4] 安装PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo 错误: PyInstaller安装失败
    pause
    exit /b 1
)

echo.
echo [3/4] 清理旧文件...
if exist dist\TorrentToMagnet_GUI.exe del /f /q dist\TorrentToMagnet_GUI.exe
if exist build\TorrentToMagnet_GUI rmdir /s /q build\TorrentToMagnet_GUI

echo.
echo [4/4] 开始打包GUI版本...
pyinstaller --onefile --clean --name "TorrentToMagnet_GUI" ^
    --noconsole ^
    --add-data "requirements.txt;." ^
    torrent_to_magnet_gui.py

if errorlevel 1 (
    echo.
    echo 错误: 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 可执行文件位置: dist\TorrentToMagnet_GUI.exe
echo.
echo 使用方法:
echo   双击 TorrentToMagnet_GUI.exe 运行
echo   拖拽torrent文件到窗口即可转换
echo.
pause