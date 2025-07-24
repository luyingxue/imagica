#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI图像生成器主程序
使用 CustomTkinter 构建的轻量级图像生成器应用
"""

import sys
import os
import tkinter.messagebox as messagebox

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 初始化日志系统
from utils.logger import log_manager, get_logger, log_exception
from utils.exceptions import ImageGeneratorException
from config.constants import APP_NAME, APP_VERSION

# 获取主程序日志记录器
logger = get_logger(__name__)


def main():
    """主函数，启动应用程序"""
    try:
        logger.info(f"{APP_NAME} v{APP_VERSION} 启动中...")
        
        # 检查Python版本
        if sys.version_info < (3, 7):
            error_msg = "此应用程序需要 Python 3.7 或更高版本"
            logger.error(error_msg)
            messagebox.showerror("版本错误", error_msg)
            sys.exit(1)
        
        # 检查必要的依赖
        try:
            import customtkinter
            import requests
            import PIL
        except ImportError as e:
            error_msg = f"缺少必要的依赖包: {str(e)}\n请运行: pip install -r requirements.txt"
            logger.error(error_msg)
            messagebox.showerror("依赖错误", error_msg)
            sys.exit(1)
        
        # 导入并创建主窗口
        from ui.main_window import MainWindow
        
        logger.info("创建主窗口...")
        app = MainWindow()
        
        logger.info("应用程序启动完成，开始主循环")
        app.mainloop()
        
        logger.info("应用程序正常退出")
        
    except ImageGeneratorException as e:
        # 自定义异常处理
        error_msg = f"应用程序错误: {str(e)}"
        logger.error(error_msg)
        messagebox.showerror("应用程序错误", str(e))
        sys.exit(1)
        
    except ImportError as e:
        # 模块导入错误
        error_msg = f"模块导入失败: {str(e)}"
        log_exception(logger, e, "模块导入错误")
        messagebox.showerror("导入错误", error_msg)
        sys.exit(1)
        
    except Exception as e:
        # 未预期的错误
        error_msg = f"应用程序启动失败: {str(e)}"
        log_exception(logger, e, "未预期的启动错误")
        
        # 尝试显示错误对话框
        try:
            messagebox.showerror("启动错误", error_msg)
        except:
            # 如果连对话框都无法显示，则输出到控制台
            print(f"严重错误: {error_msg}")
        
        sys.exit(1)


def check_environment():
    """检查运行环境"""
    logger.info("检查运行环境...")
    
    # 检查操作系统
    import platform
    os_info = f"{platform.system()} {platform.release()}"
    logger.info(f"操作系统: {os_info}")
    
    # 检查Python版本
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    logger.info(f"Python版本: {python_version}")
    
    # 检查工作目录
    work_dir = os.getcwd()
    logger.info(f"工作目录: {work_dir}")
    
    # 检查关键目录
    required_dirs = ['ui', 'utils', 'config', 'assets']
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        error_msg = f"缺少必要的目录: {', '.join(missing_dirs)}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    logger.info("环境检查完成")


if __name__ == "__main__":
    # 设置异常处理
    def handle_exception(exc_type, exc_value, exc_traceback):
        """全局异常处理器"""
        if issubclass(exc_type, KeyboardInterrupt):
            # 处理Ctrl+C中断
            logger.info("用户中断程序")
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        # 记录未捕获的异常
        logger.critical("未捕获的异常", exc_info=(exc_type, exc_value, exc_traceback))
    
    # 设置全局异常处理器
    sys.excepthook = handle_exception
    
    try:
        # 检查环境
        check_environment()
        
        # 启动主程序
        main()
        
    except KeyboardInterrupt:
        logger.info("用户中断程序启动")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"程序启动前发生严重错误: {str(e)}", exc_info=True)
        try:
            messagebox.showerror("严重错误", f"程序无法启动: {str(e)}")
        except:
            print(f"严重错误: {str(e)}")
        sys.exit(1) 