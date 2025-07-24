@echo off
chcp 65001 >nul 2>&1
title AI图像生成器 - v2.0.0

echo.
echo 🎨 =====================================
echo    AI 图像生成器 - 重构优化版 v2.0.0
echo    基于 CustomTkinter 的轻量级应用
echo =====================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python 环境
    echo.
    echo 📋 解决方案：
    echo    1. 请安装 Python 3.7 或更高版本
    echo    2. 确保 Python 已添加到 PATH 环境变量
    echo    3. 重新打开命令窗口后再试
    echo.
    pause
    exit /b 1
)

:: 显示Python版本
echo 🐍 检测到 Python 版本：
python --version
echo.

:: 检查是否在项目目录
if not exist "main.py" (
    echo ❌ 错误：请在项目根目录下运行此脚本
    echo 📂 当前目录：%CD%
    echo.
    pause
    exit /b 1
)

:: 检查依赖是否安装
echo 🔍 检查依赖包...
python -c "import customtkinter, requests, PIL" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  警告：缺少必要的依赖包
    echo.
    echo 🔧 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖包安装失败
        echo.
        echo 💡 请尝试手动安装：
        echo    pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
    echo ✅ 依赖包安装完成
    echo.
)

:: 启动应用程序
echo 🚀 正在启动 AI 图像生成器...
echo.

python main.py

:: 检查退出代码
if errorlevel 1 (
    echo.
    echo ❌ 应用程序异常退出
    echo 📋 请检查错误信息或查看日志文件：logs/
    echo.
) else (
    echo.
    echo ✅ 应用程序正常退出
    echo.
)

echo 💡 提示：日志文件位于 logs/ 目录中
echo 📧 如有问题，请查看项目文档或提交 Issue
echo.
pause
