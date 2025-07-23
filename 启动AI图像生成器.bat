@echo off
chcp 65001 >nul
echo 🎨 AI图像生成器
echo ====================
echo.
echo 正在启动程序...
echo.

if exist "AI图像生成器.exe" (
    start "" "AI图像生成器.exe"
) else (
    echo ❌ 错误：找不到AI图像生成器.exe文件
    echo 请确保此批处理文件与exe文件在同一目录
    pause
)
