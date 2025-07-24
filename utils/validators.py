# -*- coding: utf-8 -*-
"""
输入验证器
提供统一的数据验证功能
"""

import re
from typing import Optional, Union
from urllib.parse import urlparse

from config.constants import VALIDATION, ERROR_MESSAGES
from utils.exceptions import ValidationException


class InputValidator:
    """输入验证器类"""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        验证API Key
        
        Args:
            api_key: API Key字符串
            
        Returns:
            验证是否通过
            
        Raises:
            ValidationException: 验证失败时抛出
        """
        if not api_key or not api_key.strip():
            raise ValidationException(ERROR_MESSAGES["no_api_key"], field="api_key", value=api_key)
        
        api_key = api_key.strip()
        
        if len(api_key) < VALIDATION["api_key_min_length"]:
            raise ValidationException(
                f"API Key 长度至少需要 {VALIDATION['api_key_min_length']} 个字符",
                field="api_key",
                value=api_key
            )
        
        if api_key.lower() in ["your-api-key-here", "test", "demo", "example"]:
            raise ValidationException(ERROR_MESSAGES["invalid_api_key"], field="api_key", value=api_key)
        
        return True
    
    @staticmethod
    def validate_prompt(prompt: str) -> bool:
        """
        验证提示词
        
        Args:
            prompt: 提示词字符串
            
        Returns:
            验证是否通过
            
        Raises:
            ValidationException: 验证失败时抛出
        """
        if not prompt or not prompt.strip():
            raise ValidationException(ERROR_MESSAGES["no_prompt"], field="prompt", value=prompt)
        
        prompt = prompt.strip()
        
        if len(prompt) < VALIDATION["prompt_min_length"]:
            raise ValidationException(
                f"描述至少需要 {VALIDATION['prompt_min_length']} 个字符",
                field="prompt",
                value=prompt
            )
        
        if len(prompt) > VALIDATION["prompt_max_length"]:
            raise ValidationException(
                f"描述不能超过 {VALIDATION['prompt_max_length']} 个字符",
                field="prompt",
                value=prompt
            )
        
        return True
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        验证URL
        
        Args:
            url: URL字符串
            
        Returns:
            验证是否通过
            
        Raises:
            ValidationException: 验证失败时抛出
        """
        if not url or not url.strip():
            raise ValidationException("URL 不能为空", field="url", value=url)
        
        url = url.strip()
        
        # 使用正则表达式验证URL格式
        url_pattern = VALIDATION["url_pattern"]
        if not re.match(url_pattern, url):
            raise ValidationException("URL 格式不正确", field="url", value=url)
        
        # 使用urllib验证URL结构
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                raise ValidationException("URL 缺少域名", field="url", value=url)
        except Exception:
            raise ValidationException("URL 格式无效", field="url", value=url)
        
        return True
    
    @staticmethod
    def validate_number_range(value: Union[int, float], min_val: Union[int, float], 
                            max_val: Union[int, float], field_name: str = "值") -> bool:
        """
        验证数值范围
        
        Args:
            value: 要验证的值
            min_val: 最小值
            max_val: 最大值
            field_name: 字段名称
            
        Returns:
            验证是否通过
            
        Raises:
            ValidationException: 验证失败时抛出
        """
        if value < min_val:
            raise ValidationException(
                f"{field_name} 不能小于 {min_val}",
                field=field_name,
                value=str(value)
            )
        
        if value > max_val:
            raise ValidationException(
                f"{field_name} 不能大于 {max_val}",
                field=field_name,
                value=str(value)
            )
        
        return True
    
    @staticmethod
    def validate_file_path(file_path: str, must_exist: bool = False) -> bool:
        """
        验证文件路径
        
        Args:
            file_path: 文件路径
            must_exist: 是否必须存在
            
        Returns:
            验证是否通过
            
        Raises:
            ValidationException: 验证失败时抛出
        """
        import os
        
        if not file_path or not file_path.strip():
            raise ValidationException("文件路径不能为空", field="file_path", value=file_path)
        
        file_path = file_path.strip()
        
        # 检查路径格式
        try:
            os.path.normpath(file_path)
        except Exception:
            raise ValidationException("文件路径格式无效", field="file_path", value=file_path)
        
        # 检查文件是否存在（如果需要）
        if must_exist and not os.path.exists(file_path):
            raise ValidationException("文件不存在", field="file_path", value=file_path)
        
        return True
    
    @staticmethod
    def validate_image_format(file_path: str) -> bool:
        """
        验证图像文件格式
        
        Args:
            file_path: 图像文件路径
            
        Returns:
            验证是否通过
            
        Raises:
            ValidationException: 验证失败时抛出
        """
        import os
        
        if not file_path:
            raise ValidationException("文件路径不能为空", field="file_path", value=file_path)
        
        # 获取文件扩展名
        _, ext = os.path.splitext(file_path.lower())
        
        if ext not in VALIDATION["supported_image_formats"]:
            supported_formats = ", ".join(VALIDATION["supported_image_formats"])
            raise ValidationException(
                f"不支持的图像格式。支持的格式: {supported_formats}",
                field="file_format",
                value=ext
            )
        
        return True
    
    @staticmethod
    def validate_generation_params(num_images: int, size: str, model: str) -> bool:
        """
        验证图像生成参数
        
        Args:
            num_images: 图像数量
            size: 图像尺寸
            model: 模型名称
            
        Returns:
            验证是否通过
            
        Raises:
            ValidationException: 验证失败时抛出
        """
        from config.constants import GENERATION_CONFIG, API_CONFIG
        
        # 验证图像数量
        InputValidator.validate_number_range(
            num_images,
            GENERATION_CONFIG["min_images"],
            GENERATION_CONFIG["max_images"],
            "图像数量"
        )
        
        # 验证图像尺寸
        if size not in API_CONFIG["sizes"]:
            valid_sizes = ", ".join(API_CONFIG["sizes"].keys())
            raise ValidationException(
                f"无效的图像尺寸。支持的尺寸: {valid_sizes}",
                field="size",
                value=size
            )
        
        # 验证模型
        if model not in API_CONFIG["models"]:
            valid_models = ", ".join(API_CONFIG["models"].keys())
            raise ValidationException(
                f"无效的模型。支持的模型: {valid_models}",
                field="model",
                value=model
            )
        
        return True


class ConfigValidator:
    """配置验证器"""
    
    @staticmethod
    def validate_config_data(config_data: dict) -> bool:
        """
        验证配置数据
        
        Args:
            config_data: 配置数据字典
            
        Returns:
            验证是否通过
            
        Raises:
            ValidationException: 验证失败时抛出
        """
        if not isinstance(config_data, dict):
            raise ValidationException("配置数据必须是字典格式", field="config", value=str(type(config_data)))
        
        # 验证API Key（如果存在）
        if "api_key" in config_data and config_data["api_key"]:
            InputValidator.validate_api_key(config_data["api_key"])
        
        # 验证API URL（如果存在）
        if "api_url" in config_data and config_data["api_url"]:
            InputValidator.validate_url(config_data["api_url"])
        
        return True
    
    @staticmethod
    def validate_log_config(log_config: dict) -> bool:
        """
        验证日志配置
        
        Args:
            log_config: 日志配置字典
            
        Returns:
            验证是否通过
            
        Raises:
            ValidationException: 验证失败时抛出
        """
        import logging
        
        if not isinstance(log_config, dict):
            raise ValidationException("日志配置必须是字典格式", field="log_config", value=str(type(log_config)))
        
        # 验证日志级别
        if "level" in log_config:
            level = log_config["level"]
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if level not in valid_levels:
                raise ValidationException(
                    f"无效的日志级别。支持的级别: {', '.join(valid_levels)}",
                    field="log_level",
                    value=level
                )
        
        # 验证文件大小限制
        if "max_size" in log_config:
            max_size = log_config["max_size"]
            if not isinstance(max_size, (int, float)) or max_size <= 0:
                raise ValidationException(
                    "日志文件最大大小必须是正数",
                    field="max_size",
                    value=str(max_size)
                )
        
        return True


# 便捷验证函数
def validate_user_input(api_key: str, prompt: str, api_url: str) -> bool:
    """
    验证用户输入的便捷函数
    
    Args:
        api_key: API Key
        prompt: 提示词
        api_url: API URL
        
    Returns:
        验证是否通过
        
    Raises:
        ValidationException: 验证失败时抛出
    """
    InputValidator.validate_api_key(api_key)
    InputValidator.validate_prompt(prompt)
    InputValidator.validate_url(api_url)
    return True


def validate_generation_request(num_images: int, size: str, model: str, prompt: str) -> bool:
    """
    验证图像生成请求的便捷函数
    
    Args:
        num_images: 图像数量
        size: 图像尺寸
        model: 模型名称
        prompt: 提示词
        
    Returns:
        验证是否通过
        
    Raises:
        ValidationException: 验证失败时抛出
    """
    InputValidator.validate_generation_params(num_images, size, model)
    InputValidator.validate_prompt(prompt)
    return True 