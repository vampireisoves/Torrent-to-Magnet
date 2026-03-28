@echo off
chcp 65001 >nul
echo ========================================
echo Torrent转Magnet工具 - CLI版本打包脚本
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
echo [3/4] 可选: 安装pyperclip（剪贴板支持）...
pip install pyperclip

echo.
echo [4/4] 开始打包...
pyinstaller --onefile --clean --name "TorrentToMagnet" ^
    --add-data "requirements.txt;." ^
    --icon=NONE ^
    torrent_to_magnet.py

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
echo 可执行文件位置: dist\TorrentToMagnet.exe
echo.
echo 使用方法:
echo   1. 双击 TorrentToMagnet.exe 查看帮助
echo   2. 拖拽 .torrent 文件到 exe 上
echo   3. 命令行: TorrentToMagnet.exe <文件路径>
echo.
pause