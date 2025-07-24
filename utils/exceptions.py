# -*- coding: utf-8 -*-
"""
自定义异常类
定义应用程序特定的异常类型
"""

from typing import Optional


class ImageGeneratorException(Exception):
    """图像生成器基础异常类"""
    
    def __init__(self, message: str, code: Optional[str] = None, details: Optional[dict] = None):
        """
        初始化异常
        
        Args:
            message: 错误消息
            code: 错误代码
            details: 错误详情
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class APIException(ImageGeneratorException):
    """API相关异常"""
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 response_text: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.status_code = status_code
        self.response_text = response_text


class APIKeyException(APIException):
    """API Key相关异常"""
    pass


class APITimeoutException(APIException):
    """API超时异常"""
    pass


class NetworkException(ImageGeneratorException):
    """网络连接异常"""
    pass


class ConfigException(ImageGeneratorException):
    """配置相关异常"""
    pass


class ValidationException(ImageGeneratorException):
    """输入验证异常"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.field = field
        self.value = value


class ImageProcessingException(ImageGeneratorException):
    """图像处理异常"""
    pass


class FileOperationException(ImageGeneratorException):
    """文件操作异常"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.file_path = file_path


class UIException(ImageGeneratorException):
    """UI相关异常"""
    pass


# 异常映射表
EXCEPTION_MAPPING = {
    "api_key_invalid": APIKeyException,
    "api_timeout": APITimeoutException,
    "network_error": NetworkException,
    "config_error": ConfigException,
    "validation_error": ValidationException,
    "image_processing_error": ImageProcessingException,
    "file_operation_error": FileOperationException,
    "ui_error": UIException
}


def create_exception(exception_type: str, message: str, **kwargs) -> ImageGeneratorException:
    """
    根据类型创建异常实例
    
    Args:
        exception_type: 异常类型
        message: 错误消息
        **kwargs: 其他参数
        
    Returns:
        异常实例
    """
    exception_class = EXCEPTION_MAPPING.get(exception_type, ImageGeneratorException)
    return exception_class(message, **kwargs)


class ExceptionHandler:
    """异常处理器"""
    
    @staticmethod
    def handle_api_error(status_code: int, response_text: str) -> APIException:
        """
        处理API错误
        
        Args:
            status_code: HTTP状态码
            response_text: 响应文本
            
        Returns:
            对应的API异常
        """
        if status_code == 401:
            return APIKeyException("API Key 无效或已过期", status_code=status_code, response_text=response_text)
        elif status_code == 429:
            return APIException("API 请求频率限制", status_code=status_code, response_text=response_text)
        elif status_code == 500:
            return APIException("API 服务器内部错误", status_code=status_code, response_text=response_text)
        elif status_code >= 400:
            return APIException(f"API 请求失败: HTTP {status_code}", status_code=status_code, response_text=response_text)
        else:
            return APIException("未知API错误", status_code=status_code, response_text=response_text)
    
    @staticmethod
    def handle_network_error(error: Exception) -> NetworkException:
        """
        处理网络错误
        
        Args:
            error: 原始网络错误
            
        Returns:
            网络异常
        """
        if "timeout" in str(error).lower():
            return APITimeoutException("网络请求超时，请检查网络连接")
        elif "connection" in str(error).lower():
            return NetworkException("网络连接失败，请检查网络设置")
        else:
            return NetworkException(f"网络错误: {str(error)}")
    
    @staticmethod
    def handle_validation_error(field: str, value: str, rule: str) -> ValidationException:
        """
        处理验证错误
        
        Args:
            field: 字段名
            value: 字段值
            rule: 验证规则
            
        Returns:
            验证异常
        """
        if rule == "required":
            return ValidationException(f"{field} 不能为空", field=field, value=value)
        elif rule == "min_length":
            return ValidationException(f"{field} 长度不足", field=field, value=value)
        elif rule == "max_length":
            return ValidationException(f"{field} 长度超限", field=field, value=value)
        elif rule == "pattern":
            return ValidationException(f"{field} 格式不正确", field=field, value=value)
        else:
            return ValidationException(f"{field} 验证失败: {rule}", field=field, value=value)
    
    @staticmethod
    def handle_file_error(operation: str, file_path: str, error: Exception) -> FileOperationException:
        """
        处理文件操作错误
        
        Args:
            operation: 操作类型
            file_path: 文件路径
            error: 原始错误
            
        Returns:
            文件操作异常
        """
        if "permission" in str(error).lower():
            return FileOperationException(f"没有权限{operation}文件: {file_path}", file_path=file_path)
        elif "not found" in str(error).lower():
            return FileOperationException(f"文件不存在: {file_path}", file_path=file_path)
        elif "space" in str(error).lower():
            return FileOperationException(f"磁盘空间不足，无法{operation}文件: {file_path}", file_path=file_path)
        else:
            return FileOperationException(f"{operation}文件失败: {str(error)}", file_path=file_path) 