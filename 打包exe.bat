@echo off
chcp 65001 >nul
title AI图像生成器 - 打包工具

echo.
echo 🎨 AI图像生成器 - 打包工具
echo ================================
echo.

echo 📦 正在检查PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller未安装，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller安装失败！
        pause
        exit /b 1
    )
    echo ✅ PyInstaller安装成功
) else (
    echo ✅ PyInstaller已安装
)

echo.
echo 🧹 清理之前的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
for %%f in (*.spec) do del "%%f"

echo.
echo 🚀 开始构建exe文件...

REM 检查图标文件
if exist "assets\icon.ico" (
    set ICON_OPTION=--icon=assets\icon.ico
    echo ✅ 使用图标文件: assets\icon.ico
) else (
    set ICON_OPTION=
    echo ⚠️ 图标文件不存在，使用默认图标
)

REM 执行PyInstaller命令
pyinstaller --onefile --windowed --name="AI图像生成器" --add-data="assets;assets" --hidden-import=PyQt5.sip --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtWidgets --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=openai --hidden-import=requests --clean --noconfirm %ICON_OPTION% main.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败！
    echo.
    echo 💡 常见解决方案:
    echo 1. 确保所有依赖包已正确安装
    echo 2. 尝试以管理员身份运行此批处理文件
    echo 3. 检查防病毒软件是否阻止了打包过程
    echo 4. 确保在项目根目录下运行
    pause
    exit /b 1
)

echo.
echo 🎉 打包完成！
echo 📁 exe文件位置: dist\AI图像生成器.exe

REM 检查文件大小
if exist "dist\AI图像生成器.exe" (
    for %%A in ("dist\AI图像生成器.exe") do set SIZE=%%~zA
    set /a SIZE_MB=%SIZE%/1024/1024
    echo 📊 exe文件大小: %SIZE_MB% MB
)

echo.
echo 📋 使用说明:
echo 1. 将 dist\AI图像生成器.exe 复制到目标位置
echo 2. 将 assets 文件夹复制到exe文件同目录
echo 3. 确保目标机器有网络连接
echo 4. 首次运行需要配置OpenAI API Key
echo.

echo 是否要打开dist文件夹？(Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    explorer dist
)

pause 