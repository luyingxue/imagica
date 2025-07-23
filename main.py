#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像生成器主程序
使用 PyQt5 和 OpenAI API 构建的本地图像生成器应用
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# 设置高 DPI 缩放属性（必须在创建 QApplication 之前）
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def main():
    """主函数，启动应用程序"""
    # 创建 QApplication 实例
    app = QApplication(sys.argv)
    app.setApplicationName("AI 图像生成器")
    app.setApplicationVersion("1.0.0")
    
    try:
        # 创建主窗口
        main_window = MainWindow()
        main_window.show()
        
        # 运行应用程序主循环
        sys.exit(app.exec_())
        
    except Exception as e:
        # 错误处理
        error_msg = f"应用程序启动失败: {str(e)}"
        print(error_msg)
        
        # 如果可能的话显示错误对话框
        try:
            QMessageBox.critical(None, "启动错误", error_msg)
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main() 