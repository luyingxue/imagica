#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 将AI图像生成器打包成exe文件
使用PyInstaller进行打包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
        return True
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyInstaller安装失败")
            return False

def clean_build_dirs():
    """清理之前的构建目录"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 清理spec文件
    spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]
    for spec_file in spec_files:
        print(f"🧹 删除文件: {spec_file}")
        os.remove(spec_file)

def build_exe():
    """构建exe文件"""
    print("🚀 开始构建exe文件...")
    
    # PyInstaller命令参数
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个exe文件
        "--windowed",                   # 不显示控制台窗口
        "--name=AI图像生成器",           # 设置exe文件名
        "--icon=assets/icon.ico",       # 设置图标
        "--add-data=assets;assets",     # 包含资源文件
        "--hidden-import=PyQt5.sip",    # 包含PyQt5.sip模块
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui", 
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=openai",
        "--hidden-import=requests",
        "--clean",                      # 清理临时文件
        "--noconfirm",                  # 不询问确认
        "main.py"                       # 主程序文件
    ]
    
    try:
        # 执行PyInstaller命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ exe文件构建成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def create_installer():
    """创建安装包（可选）"""
    print("📦 创建安装包...")
    
    # 检查是否有Inno Setup
    try:
        subprocess.run(["iscc", "/?"], check=True, capture_output=True)
        print("✅ 检测到Inno Setup，创建安装包...")
        
        # 创建Inno Setup脚本
        inno_script = """
[Setup]
AppName=AI图像生成器
AppVersion=1.0.0
DefaultDirName={pf}\\AI图像生成器
DefaultGroupName=AI图像生成器
OutputDir=dist
OutputBaseFilename=AI图像生成器_安装包
SetupIconFile=assets\\icon.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Languages\\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\AI图像生成器.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\\*"; DestDir: "{app}\\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\AI图像生成器"; Filename: "{app}\\AI图像生成器.exe"
Name: "{commondesktop}\\AI图像生成器"; Filename: "{app}\\AI图像生成器.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\AI图像生成器.exe"; Description: "{cm:LaunchProgram,AI图像生成器}"; Flags: nowait postinstall skipifsilent
"""
        
        with open("installer.iss", "w", encoding="utf-8") as f:
            f.write(inno_script)
        
        # 执行Inno Setup
        subprocess.run(["iscc", "installer.iss"], check=True)
        print("✅ 安装包创建成功！")
        
        # 清理临时文件
        os.remove("installer.iss")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ 未检测到Inno Setup，跳过安装包创建")

def main():
    """主函数"""
    print("🎨 AI图像生成器 - 打包工具")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists("main.py"):
        print("❌ 错误：请在项目根目录下运行此脚本")
        return
    
    # 检查PyInstaller
    if not check_pyinstaller():
        return
    
    # 清理之前的构建
    clean_build_dirs()
    
    # 构建exe
    if build_exe():
        print("\n🎉 打包完成！")
        print("📁 exe文件位置: dist/AI图像生成器.exe")
        
        # 尝试创建安装包
        create_installer()
        
        print("\n📋 使用说明:")
        print("1. 将生成的exe文件复制到目标机器")
        print("2. 确保目标机器有网络连接（用于调用OpenAI API）")
        print("3. 首次运行时需要配置API Key")
        print("4. 建议将assets文件夹与exe文件放在同一目录")
        
    else:
        print("❌ 打包失败，请检查错误信息")

if __name__ == "__main__":
    main() 