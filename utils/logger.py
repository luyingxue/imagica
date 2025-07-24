# -*- coding: utf-8 -*-
"""
日志管理器
提供应用程序的统一日志记录功能
"""

import os
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional

from config.constants import LOG_CONFIG, PATHS


class LogManager:
    """日志管理器类"""
    
    _instance: Optional['LogManager'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'LogManager':
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化日志管理器"""
        if not self._initialized:
            self._setup_logging()
            self._initialized = True
    
    def _setup_logging(self) -> None:
        """设置日志配置"""
        try:
            # 创建日志目录
            log_dir = Path(PATHS["log_dir"])
            log_dir.mkdir(exist_ok=True)
            
            # 设置日志文件路径
            log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
            
            # 创建根日志记录器
            root_logger = logging.getLogger()
            root_logger.setLevel(getattr(logging, LOG_CONFIG["level"]))
            
            # 清除现有的处理器
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)
            
            # 创建文件处理器（轮转日志）
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=LOG_CONFIG["max_size"],
                backupCount=LOG_CONFIG["backup_count"],
                encoding=LOG_CONFIG["encoding"]
            )
            file_handler.setLevel(logging.DEBUG)
            
            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 创建格式器
            formatter = logging.Formatter(LOG_CONFIG["format"])
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # 添加处理器到根日志记录器
            root_logger.addHandler(file_handler)
            root_logger.addHandler(console_handler)
            
            # 记录初始化成功
            logging.info("日志系统初始化成功")
            
        except Exception as e:
            print(f"日志系统初始化失败: {e}")
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        获取指定名称的日志记录器
        
        Args:
            name: 日志记录器名称
            
        Returns:
            日志记录器实例
        """
        return logging.getLogger(name)
    
    @staticmethod
    def log_exception(logger: logging.Logger, exception: Exception, context: str = "") -> None:
        """
        记录异常信息
        
        Args:
            logger: 日志记录器
            exception: 异常对象
            context: 异常上下文描述
        """
        if context:
            logger.error(f"{context}: {type(exception).__name__}: {str(exception)}", exc_info=True)
        else:
            logger.error(f"{type(exception).__name__}: {str(exception)}", exc_info=True)
    
    @staticmethod
    def log_api_request(logger: logging.Logger, url: str, method: str = "POST", 
                       status_code: Optional[int] = None, response_time: Optional[float] = None) -> None:
        """
        记录API请求信息
        
        Args:
            logger: 日志记录器
            url: 请求URL
            method: 请求方法
            status_code: 响应状态码
            response_time: 响应时间（秒）
        """
        if status_code and response_time:
            logger.info(f"API请求: {method} {url} - 状态码: {status_code} - 耗时: {response_time:.2f}s")
        else:
            logger.info(f"API请求: {method} {url}")
    
    @staticmethod
    def log_user_action(logger: logging.Logger, action: str, details: str = "") -> None:
        """
        记录用户操作
        
        Args:
            logger: 日志记录器
            action: 操作名称
            details: 操作详情
        """
        if details:
            logger.info(f"用户操作: {action} - {details}")
        else:
            logger.info(f"用户操作: {action}")
    
    @staticmethod
    def log_performance(logger: logging.Logger, operation: str, duration: float, 
                       memory_usage: Optional[float] = None) -> None:
        """
        记录性能信息
        
        Args:
            logger: 日志记录器
            operation: 操作名称
            duration: 操作耗时（秒）
            memory_usage: 内存使用量（MB）
        """
        if memory_usage:
            logger.info(f"性能: {operation} - 耗时: {duration:.2f}s - 内存: {memory_usage:.1f}MB")
        else:
            logger.info(f"性能: {operation} - 耗时: {duration:.2f}s")


# 全局日志管理器实例
log_manager = LogManager()

# 便捷函数
def get_logger(name: str) -> logging.Logger:
    """获取日志记录器的便捷函数"""
    return LogManager.get_logger(name)

def log_exception(logger: logging.Logger, exception: Exception, context: str = "") -> None:
    """记录异常的便捷函数"""
    LogManager.log_exception(logger, exception, context)

def log_api_request(logger: logging.Logger, url: str, method: str = "POST", 
                   status_code: Optional[int] = None, response_time: Optional[float] = None) -> None:
    """记录API请求的便捷函数"""
    LogManager.log_api_request(logger, url, method, status_code, response_time)

def log_user_action(logger: logging.Logger, action: str, details: str = "") -> None:
    """记录用户操作的便捷函数"""
    LogManager.log_user_action(logger, action, details)

def log_performance(logger: logging.Logger, operation: str, duration: float, 
                   memory_usage: Optional[float] = None) -> None:
    """记录性能信息的便捷函数"""
    LogManager.log_performance(logger, operation, duration, memory_usage) 