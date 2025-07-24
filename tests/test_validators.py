# -*- coding: utf-8 -*-
"""
验证器模块测试
"""

import pytest

from utils.validators import InputValidator, ConfigValidator
from utils.exceptions import ValidationException


class TestInputValidator:
    """输入验证器测试类"""
    
    def test_valid_api_key(self):
        """测试有效的API Key"""
        valid_keys = [
            "sk-1234567890abcdef",
            "test_key_with_length",
            "a" * 20
        ]
        
        for key in valid_keys:
            assert InputValidator.validate_api_key(key) is True
    
    def test_invalid_api_key(self):
        """测试无效的API Key"""
        invalid_keys = [
            "",
            "   ",
            "short",
            "your-api-key-here",
            "test",
            "demo",
            "example"
        ]
        
        for key in invalid_keys:
            with pytest.raises(ValidationException):
                InputValidator.validate_api_key(key)
    
    def test_valid_prompt(self):
        """测试有效的提示词"""
        valid_prompts = [
            "一只可爱的小猫",
            "A beautiful landscape",
            "test prompt"
        ]
        
        for prompt in valid_prompts:
            assert InputValidator.validate_prompt(prompt) is True
    
    def test_invalid_prompt(self):
        """测试无效的提示词"""
        invalid_prompts = [
            "",
            "   ",
            "123",  # 太短
            "a" * 1001  # 太长
        ]
        
        for prompt in invalid_prompts:
            with pytest.raises(ValidationException):
                InputValidator.validate_prompt(prompt)
    
    def test_valid_url(self):
        """测试有效的URL"""
        valid_urls = [
            "https://api.example.com",
            "http://localhost:8080/api",
            "https://api.openai.com/v1/images"
        ]
        
        for url in valid_urls:
            assert InputValidator.validate_url(url) is True
    
    def test_invalid_url(self):
        """测试无效的URL"""
        invalid_urls = [
            "",
            "   ",
            "not_a_url",
            "ftp://example.com",
            "https://",
            "http://"
        ]
        
        for url in invalid_urls:
            with pytest.raises(ValidationException):
                InputValidator.validate_url(url)
    
    def test_number_range_validation(self):
        """测试数值范围验证"""
        # 有效范围
        assert InputValidator.validate_number_range(5, 1, 10) is True
        assert InputValidator.validate_number_range(1, 1, 10) is True
        assert InputValidator.validate_number_range(10, 1, 10) is True
        
        # 无效范围
        with pytest.raises(ValidationException):
            InputValidator.validate_number_range(0, 1, 10)
        
        with pytest.raises(ValidationException):
            InputValidator.validate_number_range(11, 1, 10)
    
    def test_generation_params_validation(self):
        """测试图像生成参数验证"""
        # 有效参数
        assert InputValidator.validate_generation_params(3, "1024x1536", "sora_image") is True
        
        # 无效图像数量
        with pytest.raises(ValidationException):
            InputValidator.validate_generation_params(0, "1024x1536", "sora_image")
        
        with pytest.raises(ValidationException):
            InputValidator.validate_generation_params(10, "1024x1536", "sora_image")
        
        # 无效尺寸
        with pytest.raises(ValidationException):
            InputValidator.validate_generation_params(3, "invalid_size", "sora_image")
        
        # 无效模型
        with pytest.raises(ValidationException):
            InputValidator.validate_generation_params(3, "1024x1536", "invalid_model")


class TestConfigValidator:
    """配置验证器测试类"""
    
    def test_valid_config_data(self):
        """测试有效的配置数据"""
        valid_configs = [
            {},
            {"api_key": "test_api_key_12345"},
            {"api_url": "https://api.example.com"},
            {
                "api_key": "test_api_key_12345",
                "api_url": "https://api.example.com"
            }
        ]
        
        for config in valid_configs:
            assert ConfigValidator.validate_config_data(config) is True
    
    def test_invalid_config_data(self):
        """测试无效的配置数据"""
        invalid_configs = [
            "not_a_dict",
            123,
            [],
            {"api_key": "short"},  # API Key太短
            {"api_url": "not_a_url"}  # 无效URL
        ]
        
        for config in invalid_configs:
            with pytest.raises(ValidationException):
                ConfigValidator.validate_config_data(config)
    
    def test_log_config_validation(self):
        """测试日志配置验证"""
        # 有效配置
        valid_log_configs = [
            {},
            {"level": "INFO"},
            {"level": "DEBUG", "max_size": 1024000}
        ]
        
        for config in valid_log_configs:
            assert ConfigValidator.validate_log_config(config) is True
        
        # 无效配置
        invalid_log_configs = [
            "not_a_dict",
            {"level": "INVALID_LEVEL"},
            {"max_size": -1},
            {"max_size": "not_a_number"}
        ]
        
        for config in invalid_log_configs:
            with pytest.raises(ValidationException):
                ConfigValidator.validate_log_config(config) 