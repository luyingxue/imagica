# -*- coding: utf-8 -*-
"""
配置管理器
处理应用程序配置的持久化存储
"""

import os
import json
from typing import Optional, Dict, Any


class ConfigManager:
    """配置管理器类"""
    
    def __init__(self, config_file: str = ".apikey"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    print(f"已加载配置文件: {self.config_file}")
                    return config
            else:
                print(f"配置文件不存在，将创建新文件: {self.config_file}")
                return {}
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            return {}
    
    def save_config(self) -> bool:
        """
        保存配置文件
        
        Returns:
            保存成功返回 True，失败返回 False
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"配置文件已保存: {self.config_file}")
            return True
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            return False
    
    def get_api_key(self) -> Optional[str]:
        """
        获取 API Key
        
        Returns:
            API Key 字符串，如果不存在返回 None
        """
        return self.config.get('api_key')
    
    def set_api_key(self, api_key: str) -> bool:
        """
        设置 API Key
        
        Args:
            api_key: API Key 字符串
            
        Returns:
            设置成功返回 True，失败返回 False
        """
        try:
            self.config['api_key'] = api_key
            return self.save_config()
        except Exception as e:
            print(f"设置 API Key 失败: {str(e)}")
            return False
    
    def get_api_url(self) -> str:
        """
        获取 API URL
        
        Returns:
            API URL 字符串
        """
        return self.config.get('api_url', 'https://api.apicore.ai/v1/images/generations')
    
    def set_api_url(self, api_url: str) -> bool:
        """
        设置 API URL
        
        Args:
            api_url: API URL 字符串
            
        Returns:
            设置成功返回 True，失败返回 False
        """
        try:
            self.config['api_url'] = api_url
            return self.save_config()
        except Exception as e:
            print(f"设置 API URL 失败: {str(e)}")
            return False
    

    
    def clear_config(self) -> bool:
        """
        清除所有配置
        
        Returns:
            清除成功返回 True，失败返回 False
        """
        try:
            self.config = {}
            return self.save_config()
        except Exception as e:
            print(f"清除配置失败: {str(e)}")
            return False
    
    def is_api_key_valid(self) -> bool:
        """
        检查 API Key 是否有效
        
        Returns:
            API Key 存在且不为空返回 True
        """
        api_key = self.get_api_key()
        return api_key is not None and api_key.strip() != '' and api_key != 'your-api-key-here'


# 全局配置管理器实例
config_manager = ConfigManager() 