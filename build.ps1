# Torrent转Magnet工具 - PowerShell打包脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Torrent转Magnet工具 - 打包脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python是否安装
try {
    $pythonVersion = python --version 2>&1
    Write-Host "检测到 Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: 未找到Python，请先安装Python 3.7+" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 安装依赖
Write-Host "[1/4] 安装依赖..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 依赖安装失败" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 安装PyInstaller
Write-Host ""
Write-Host "[2/4] 安装PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: PyInstaller安装失败" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 可选: 安装pyperclip
Write-Host ""
Write-Host "[3/4] 可选: 安装pyperclip（剪贴板支持）..." -ForegroundColor Yellow
pip install pyperclip

# 打包
Write-Host ""
Write-Host "[4/4] 开始打包..." -ForegroundColor Yellow
pyinstaller --onefile --clean --name "TorrentToMagnet" `
    --add-data "requirements.txt;." `
    torrent_to_magnet.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "错误: 打包失败" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "打包完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "可执行文件位置: dist\TorrentToMagnet.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "使用方法:" -ForegroundColor Yellow
Write-Host "  1. 双击 TorrentToMagnet.exe 查看帮助" -ForegroundColor White
Write-Host "  2. 拖拽 .torrent 文件到 exe 上" -ForegroundColor White
Write-Host "  3. 命令行: TorrentToMagnet.exe <文件路径>" -ForegroundColor White
Write-Host ""

Read-Host "按回车键退出"