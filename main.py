#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI图像生成器主程序
使用 CustomTkinter 构建的轻量级图像生成器应用
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def main():
    """主函数，启动应用程序"""
    try:
        print("🎨 AI图像生成器启动中...")
        
        # 创建并运行主窗口
        app = MainWindow()
        app.mainloop()
        
    except Exception as e:
        # 错误处理
        error_msg = f"应用程序启动失败: {str(e)}"
        print(f"❌ {error_msg}")
        
        # 尝试显示错误对话框
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror("启动错误", error_msg)
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main() 