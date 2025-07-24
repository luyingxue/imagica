# -*- coding: utf-8 -*-
"""
配置模块测试
"""

import os
import json
import pytest
import tempfile
from unittest.mock import patch

from utils.config_manager import ConfigManager


class TestConfigManager:
    """配置管理器测试类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
        self.config_manager = ConfigManager(self.config_file)
    
    def teardown_method(self):
        """每个测试方法后的清理"""
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
    
    def test_load_empty_config(self):
        """测试加载空配置"""
        assert self.config_manager.config == {}
    
    def test_save_and_load_config(self):
        """测试保存和加载配置"""
        # 设置配置
        self.config_manager.config = {"test_key": "test_value"}
        
        # 保存配置
        assert self.config_manager.save_config() is True
        assert os.path.exists(self.config_file)
        
        # 创建新的配置管理器并加载
        new_config_manager = ConfigManager(self.config_file)
        assert new_config_manager.config["test_key"] == "test_value"
    
    def test_api_key_operations(self):
        """测试API Key操作"""
        # 测试设置API Key
        assert self.config_manager.set_api_key("test_api_key") is True
        assert self.config_manager.get_api_key() == "test_api_key"
        
        # 测试是否有效
        assert self.config_manager.is_api_key_valid() is True
    
    def test_api_url_operations(self):
        """测试API URL操作"""
        # 测试默认URL
        assert "api.apicore.ai" in self.config_manager.get_api_url()
        
        # 测试设置URL
        test_url = "https://test.example.com/api"
        assert self.config_manager.set_api_url(test_url) is True
        assert self.config_manager.get_api_url() == test_url
    
    def test_invalid_api_key(self):
        """测试无效的API Key"""
        # 空API Key
        self.config_manager.set_api_key("")
        assert self.config_manager.is_api_key_valid() is False
        
        # 默认API Key
        self.config_manager.set_api_key("your-api-key-here")
        assert self.config_manager.is_api_key_valid() is False
    
    def test_clear_config(self):
        """测试清除配置"""
        # 设置一些配置
        self.config_manager.set_api_key("test_key")
        self.config_manager.set_api_url("test_url")
        
        # 清除配置
        assert self.config_manager.clear_config() is True
        assert self.config_manager.config == {}
        assert self.config_manager.get_api_key() is None
    
    @patch('builtins.open', side_effect=PermissionError())
    def test_save_config_permission_error(self, mock_open):
        """测试保存配置时的权限错误"""
        assert self.config_manager.save_config() is False
    
    def test_load_invalid_json(self):
        """测试加载无效的JSON文件"""
        # 创建无效的JSON文件
        with open(self.config_file, 'w') as f:
            f.write("invalid json content")
        
        # 创建新的配置管理器
        config_manager = ConfigManager(self.config_file)
        assert config_manager.config == {}  # 应该返回空配置 