#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化打包脚本 - 将AI图像生成器打包成exe文件
专门针对Windows环境优化
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """安装PyInstaller"""
    print("📦 正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyInstaller安装失败")
        return False

def clean_previous_build():
    """清理之前的构建文件"""
    print("🧹 清理之前的构建文件...")
    
    # 删除构建目录
    for dir_name in ["build", "dist", "__pycache__"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   删除目录: {dir_name}")
    
    # 删除spec文件
    for file_name in os.listdir("."):
        if file_name.endswith(".spec"):
            os.remove(file_name)
            print(f"   删除文件: {file_name}")

def build_exe():
    """构建exe文件"""
    print("🚀 开始构建exe文件...")
    
    # 检查图标文件是否存在
    icon_path = "assets/icon.ico"
    if not os.path.exists(icon_path):
        print(f"⚠️ 图标文件不存在: {icon_path}")
        icon_option = []
    else:
        icon_option = ["--icon=" + icon_path]
    
    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",                    # 单文件模式
        "--windowed",                   # 无控制台窗口
        "--name=AI图像生成器",           # 程序名称
        "--add-data=assets;assets",     # 包含资源文件
        "--hidden-import=PyQt5.sip",    # 必需的隐藏导入
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=openai",
        "--hidden-import=requests",
        "--clean",                      # 清理缓存
        "--noconfirm",                  # 不询问确认
        "main.py"                       # 主程序
    ]
    
    # 添加图标选项
    cmd.extend(icon_option)
    
    print("执行命令:", " ".join(cmd))
    
    try:
        # 执行PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print("✅ exe文件构建成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        if e.stderr:
            print("错误信息:")
            print(e.stderr)
        return False

def create_batch_file():
    """创建批处理文件用于快速运行"""
    batch_content = """@echo off
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
"""
    
    with open("启动AI图像生成器.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    print("✅ 创建启动批处理文件: 启动AI图像生成器.bat")

def main():
    """主函数"""
    print("🎨 AI图像生成器 - 打包工具")
    print("=" * 40)
    
    # 检查是否在正确的目录
    if not os.path.exists("main.py"):
        print("❌ 错误：请在项目根目录下运行此脚本")
        print("   当前目录:", os.getcwd())
        return
    
    # 检查并安装PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
    except ImportError:
        if not install_pyinstaller():
            return
    
    # 清理之前的构建
    clean_previous_build()
    
    # 构建exe
    if build_exe():
        print("\n🎉 打包完成！")
        print("📁 exe文件位置: dist/AI图像生成器.exe")
        
        # 创建启动批处理文件
        create_batch_file()
        
        print("\n📋 使用说明:")
        print("1. 将 dist/AI图像生成器.exe 复制到目标位置")
        print("2. 将 assets 文件夹复制到exe文件同目录")
        print("3. 确保目标机器有网络连接")
        print("4. 首次运行需要配置OpenAI API Key")
        print("5. 可以使用 启动AI图像生成器.bat 快速启动")
        
        # 检查文件大小
        exe_path = "dist/AI图像生成器.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📊 exe文件大小: {size_mb:.1f} MB")
        
    else:
        print("❌ 打包失败，请检查错误信息")
        print("\n💡 常见解决方案:")
        print("1. 确保所有依赖包已正确安装")
        print("2. 尝试以管理员身份运行")
        print("3. 检查防病毒软件是否阻止了打包过程")

if __name__ == "__main__":
    main() 