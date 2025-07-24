# -*- coding: utf-8 -*-
"""
配置管理器
处理应用程序配置的持久化存储
"""

import os
import json
from typing import Optional, Dict, Any

from config.constants import PATHS, ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.logger import get_logger, log_exception
from utils.exceptions import ConfigException, FileOperationException, ValidationException


class ConfigManager:
    """配置管理器类"""
    
    def __init__(self, config_file: str = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，默认使用常量中定义的路径
        """
        self.config_file = config_file or PATHS["config_file"]
        self.logger = get_logger(__name__)
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
            
        Raises:
            ConfigException: 配置加载失败时抛出
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.logger.info(f"配置文件加载成功: {self.config_file}")
                    return config
            else:
                self.logger.info(f"配置文件不存在，将使用默认配置: {self.config_file}")
                return {}
        except json.JSONDecodeError as e:
            error_msg = f"配置文件格式错误: {str(e)}"
            self.logger.error(error_msg)
            raise ConfigException(error_msg, code="invalid_json", details={"file": self.config_file})
        except PermissionError as e:
            error_msg = f"没有权限读取配置文件: {self.config_file}"
            log_exception(self.logger, e, "读取配置文件失败")
            raise FileOperationException(error_msg, file_path=self.config_file)
        except Exception as e:
            error_msg = f"加载配置文件失败: {str(e)}"
            log_exception(self.logger, e, "配置文件加载异常")
            raise ConfigException(error_msg, details={"file": self.config_file})
    
    def save_config(self) -> bool:
        """
        保存配置文件
        
        Returns:
            保存成功返回 True，失败返回 False
            
        Raises:
            ConfigException: 配置保存失败时抛出
        """
        try:
            # 确保目录存在
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"配置文件保存成功: {self.config_file}")
            return True
            
        except PermissionError as e:
            error_msg = f"没有权限写入配置文件: {self.config_file}"
            log_exception(self.logger, e, "保存配置文件失败")
            raise FileOperationException(error_msg, file_path=self.config_file)
        except OSError as e:
            error_msg = f"磁盘空间不足或路径无效: {self.config_file}"
            log_exception(self.logger, e, "保存配置文件失败")
            raise FileOperationException(error_msg, file_path=self.config_file)
        except Exception as e:
            error_msg = f"保存配置文件失败: {str(e)}"
            log_exception(self.logger, e, "配置文件保存异常")
            raise ConfigException(error_msg, details={"file": self.config_file})
    
    def get_api_key(self) -> Optional[str]:
        """
        获取 API Key
        
        Returns:
            API Key 字符串，如果不存在返回 None
        """
        api_key = self.config.get('api_key')
        if api_key:
            self.logger.debug("API Key 获取成功")
        return api_key
    
    def set_api_key(self, api_key: str) -> bool:
        """
        设置 API Key
        
        Args:
            api_key: API Key 字符串
            
        Returns:
            设置成功返回 True
            
        Raises:
            ValidationException: API Key 验证失败时抛出
            ConfigException: 保存失败时抛出
        """
        if not api_key or not api_key.strip():
            raise ValidationException(ERROR_MESSAGES["no_api_key"], field="api_key", value=api_key)
        
        self.config['api_key'] = api_key.strip()
        self.save_config()
        self.logger.info("API Key 设置成功")
        return True
    
    def get_api_url(self) -> str:
        """
        获取 API URL
        
        Returns:
            API URL 字符串
        """
        from config.constants import API_CONFIG
        return self.config.get('api_url', API_CONFIG["default_url"])
    
    def set_api_url(self, api_url: str) -> bool:
        """
        设置 API URL
        
        Args:
            api_url: API URL 字符串
            
        Returns:
            设置成功返回 True
            
        Raises:
            ValidationException: URL 验证失败时抛出
            ConfigException: 保存失败时抛出
        """
        if not api_url or not api_url.strip():
            raise ValidationException("API URL 不能为空", field="api_url", value=api_url)
        
        # 基本URL格式验证
        api_url = api_url.strip()
        if not (api_url.startswith('http://') or api_url.startswith('https://')):
            raise ValidationException("API URL 必须以 http:// 或 https:// 开头", field="api_url", value=api_url)
        
        self.config['api_url'] = api_url
        self.save_config()
        self.logger.info("API URL 设置成功")
        return True
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        设置配置项
        
        Args:
            key: 配置键
            value: 配置值
            
        Returns:
            设置成功返回 True
            
        Raises:
            ConfigException: 保存失败时抛出
        """
        self.config[key] = value
        self.save_config()
        self.logger.debug(f"配置项设置成功: {key}")
        return True
    
    def remove(self, key: str) -> bool:
        """
        删除配置项
        
        Args:
            key: 配置键
            
        Returns:
            删除成功返回 True
        """
        if key in self.config:
            del self.config[key]
            self.save_config()
            self.logger.debug(f"配置项删除成功: {key}")
            return True
        
        self.logger.warning(f"尝试删除不存在的配置项: {key}")
        return False
    
    def clear_config(self) -> bool:
        """
        清除所有配置
        
        Returns:
            清除成功返回 True
            
        Raises:
            ConfigException: 保存失败时抛出
        """
        self.config = {}
        self.save_config()
        self.logger.info("所有配置已清除")
        return True
    
    def is_api_key_valid(self) -> bool:
        """
        检查 API Key 是否有效
        
        Returns:
            API Key 存在且不为空返回 True
        """
        api_key = self.get_api_key()
        is_valid = (api_key is not None and 
                   api_key.strip() != '' and 
                   api_key != 'your-api-key-here' and
                   len(api_key.strip()) >= 8)
        
        if is_valid:
            self.logger.debug("API Key 验证通过")
        else:
            self.logger.warning("API Key 验证失败")
            
        return is_valid
    
    def get_all_config(self) -> Dict[str, Any]:
        """
        获取所有配置
        
        Returns:
            完整的配置字典
        """
        return self.config.copy()
    
    def update_config(self, new_config: Dict[str, Any]) -> bool:
        """
        批量更新配置
        
        Args:
            new_config: 新的配置字典
            
        Returns:
            更新成功返回 True
            
        Raises:
            ValidationException: 配置验证失败时抛出
            ConfigException: 保存失败时抛出
        """
        if not isinstance(new_config, dict):
            raise ValidationException("配置数据必须是字典格式", field="config", value=str(type(new_config)))
        
        # 验证关键配置项
        if "api_key" in new_config and new_config["api_key"]:
            # 简单验证API Key格式
            api_key = new_config["api_key"].strip()
            if len(api_key) < 8:
                raise ValidationException("API Key 长度不足", field="api_key", value=api_key)
        
        if "api_url" in new_config and new_config["api_url"]:
            # 简单验证URL格式
            api_url = new_config["api_url"].strip()
            if not (api_url.startswith('http://') or api_url.startswith('https://')):
                raise ValidationException("API URL 格式不正确", field="api_url", value=api_url)
        
        # 更新配置
        self.config.update(new_config)
        self.save_config()
        self.logger.info(f"批量更新配置成功，更新了 {len(new_config)} 个配置项")
        return True


# 全局配置管理器实例
config_manager = ConfigManager() 