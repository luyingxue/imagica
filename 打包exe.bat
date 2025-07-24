@echo off
chcp 65001 >nul 2>&1
title AI图像生成器 - 打包工具

echo.
echo 🔨 =====================================
echo    AI 图像生成器 - exe打包工具
echo    CustomTkinter轻量级版本打包
echo =====================================
echo.

:: 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python 环境
    echo 请安装 Python 3.7+ 并添加到 PATH
    echo.
    pause
    exit /b 1
)

:: 检查是否在项目根目录
if not exist "main.py" (
    echo ❌ 错误：请在项目根目录下运行此脚本
    echo.
    pause
    exit /b 1
)

:: 显示选择菜单
echo 📋 请选择打包方式：
echo.
echo   1. 完整版打包 (build_exe.py)
echo      - 功能完整，包含所有特性
echo      - 体积稍大，兼容性好
echo.
echo   2. 轻量版打包 (build_exe_simple.py)  [推荐]
echo      - 体积优化，启动更快
echo      - 适合一般用户使用
echo.
echo   3. 退出
echo.

set /p choice="请输入选择 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 🔨 开始完整版打包...
    python build_exe.py
    goto :package_done
) else if "%choice%"=="2" (
    echo.
    echo 🔨 开始轻量版打包...
    python build_exe_simple.py
    goto :package_done
) else if "%choice%"=="3" (
    echo 👋 退出打包
    goto :end
) else (
    echo ❌ 无效选择，请重新运行脚本
    pause
    exit /b 1
)

:package_done
if errorlevel 1 (
    echo.
    echo ❌ 打包失败！
    echo.
    echo 💡 常见解决方案：
    echo    1. 确保所有依赖已安装: pip install -r requirements.txt
    echo    2. 安装 PyInstaller: pip install pyinstaller
    echo    3. 以管理员身份运行此脚本
    echo    4. 检查防病毒软件是否阻止打包
    echo.
) else (
    echo.
    echo ✅ 打包完成！
    echo.
    echo 📂 输出文件位置: dist\
    echo 📊 查看文件大小和详情...
    
    if exist "dist\AI图像生成器.exe" (
        echo.
        echo 📄 文件信息：
        dir "dist\AI图像生成器.exe" | findstr "AI图像生成器.exe"
    ) else if exist "dist\AI图像生成器_轻量版.exe" (
        echo.
        echo 📄 文件信息：
        dir "dist\AI图像生成器_轻量版.exe" | findstr "AI图像生成器_轻量版.exe"
    )
    
    echo.
    echo 🎉 打包成功完成！
    echo.
    echo 📋 后续步骤：
    echo    1. 在 dist\ 目录中找到生成的 exe 文件
    echo    2. 可选：将 assets 文件夹复制到 exe 同目录
    echo    3. 测试 exe 文件是否正常运行
    echo    4. 分发给其他用户使用
    echo.
    echo 💡 提示：
    echo    - exe文件可独立运行，无需Python环境
    echo    - 首次运行需要配置API Key
    echo    - 建议在不同系统上测试兼容性
    echo.
)

:end
echo 👋 感谢使用 AI 图像生成器打包工具！
echo 📧 如有问题，请查看项目文档或提交 Issue
echo.
pause 