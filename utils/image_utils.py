# -*- coding: utf-8 -*-
"""
图像处理工具模块
包含图像生成、处理、转换和保存的相关功能
"""

import base64
import io
import os
import requests
import threading
from typing import Optional, Union, Callable
from PIL import Image, ImageTk
import tkinter as tk

from utils.config_manager import config_manager


class ImageUtils:
    """图像处理工具类"""
    
    def __init__(self, api_key: str = None):
        """
        初始化图像工具
        
        Args:
            api_key: API Key（可选，如果不提供则从配置管理器获取）
        """
        # 优先使用传入的 api_key，然后从配置管理器获取
        if api_key and api_key != 'your-api-key-here':
            self.api_key = api_key
        else:
            self.api_key = config_manager.get_api_key() or os.getenv('OPENAI_API_KEY', 'your-api-key-here')
        
        # 从配置管理器获取 API URL
        self.api_url = config_manager.get_api_url()
        
        # 打印 API Key 信息（隐藏敏感部分）
        if self.api_key and self.api_key != 'your-api-key-here':
            masked_key = self.api_key[:8] + "..." + self.api_key[-4:] if len(self.api_key) > 12 else "***"
            print(f"使用 API Key: {masked_key}")
        else:
            print("警告: 未设置有效的 API Key")
        
        # 请求头
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_image_async(self, prompt: str, size: str = "1024x1536", model: str = "sora_image", 
                           callback: Callable = None, index: int = 0) -> None:
        """
        异步调用 API 生成图像
        
        Args:
            prompt: 图像描述文本
            size: 图像尺寸，如 "1024x1536" 或 "1536x1024"
            model: 使用的模型，如 "sora_image" 或 "gpt-image-1"
            callback: 完成时的回调函数
            index: 图像索引
        """
        def generate():
            result = self.generate_image(prompt, size, model)
            if callback:
                callback(index, result)
        
        thread = threading.Thread(target=generate, daemon=True)
        thread.start()

    def generate_image(self, prompt: str, size: str = "1024x1536", model: str = "sora_image") -> Optional[str]:
        """
        调用 API 生成图像
        
        Args:
            prompt: 图像描述文本
            size: 图像尺寸，如 "1024x1536" 或 "1536x1024"
            model: 使用的模型，如 "sora_image" 或 "gpt-image-1"
            
        Returns:
            base64 编码的图像数据，失败时返回 None
        """
        try:
            # 使用固定参数
            timeout = 300  # 5分钟超时
            
            # 构建请求数据
            payload = {
                "model": model,
                "prompt": prompt,
                "n": 1,
                "size": size,
                "background": "opaque",
                "moderation": "auto",
                "output_format": "png",
                "quality": "high",
                "style": "natural",
                "output_compression": 100,
                "response_format": "b64_json"  # 添加这个字段来获取 base64 响应
            }
            
            # 打印调试信息
            print(f"发送请求到: {self.api_url}")
            print(f"⏳ 开始生成图像，超时时间设置为 {timeout} 秒...")
            
            # 发送请求
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=timeout  # 使用配置的超时时间
            )
            
            # 打印响应信息
            print(f"响应状态码: {response.status_code}")
            
            # 检查响应
            if response.status_code == 200:
                result = response.json()
                if "data" in result and len(result["data"]) > 0:
                    b64_data = result["data"][0]["b64_json"]
                    print(f"图像数据长度: {len(b64_data)} 字符")
                    return b64_data
                else:
                    print(f"API 响应中没有图像数据")
                    return None
            else:
                print(f"API 请求失败: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("API 请求超时")
            return None
        except requests.exceptions.ConnectionError:
            print("网络连接错误")
            return None
        except Exception as e:
            print(f"生成图像时发生错误: {str(e)}")
            return None

    @staticmethod
    def base64_to_tk_image(base64_data: str, size: tuple = None, use_ctk_image: bool = True) -> Optional:
        """
        将 base64 图像数据转换为 tkinter/CustomTkinter 兼容的图像
        
        Args:
            base64_data: base64 编码的图像数据
            size: 可选的图像大小 (width, height)
            use_ctk_image: 是否使用CTkImage (True) 或 PhotoImage (False)
            
        Returns:
            CTkImage 对象或 ImageTk.PhotoImage 对象，失败时返回 None
        """
        try:
            # 解码 base64 数据
            image_bytes = base64.b64decode(base64_data)
            
            # 创建 PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # 如果指定了大小，调整图像大小
            if size:
                image = image.resize(size, Image.Resampling.LANCZOS)
            
            if use_ctk_image:
                # 使用CTkImage，适用于CustomTkinter控件
                try:
                    import customtkinter as ctk
                    ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=size or image.size)
                    return ctk_image
                except Exception as e:
                    print(f"创建CTkImage失败，回退到PhotoImage: {str(e)}")
                    # 回退到PhotoImage
                    photo = ImageTk.PhotoImage(image)
                    return photo
            else:
                # 直接使用PhotoImage，适用于标准tkinter控件
                photo = ImageTk.PhotoImage(image)
                return photo
                
        except Exception as e:
            print(f"转换 base64 到图像时发生错误: {str(e)}")
            return None

    @staticmethod
    def base64_to_pil_image(base64_data: str) -> Optional[Image.Image]:
        """
        将 base64 图像数据转换为 PIL Image
        
        Args:
            base64_data: base64 编码的图像数据
            
        Returns:
            PIL Image 对象，失败时返回 None
        """
        try:
            # 解码 base64 数据
            image_bytes = base64.b64decode(base64_data)
            
            # 创建 PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            return image
            
        except Exception as e:
            print(f"转换 base64 到 PIL Image 时发生错误: {str(e)}")
            return None

    @staticmethod
    def save_base64_image(base64_data: str, file_path: str) -> bool:
        """
        保存 base64 图像数据到文件
        
        Args:
            base64_data: base64 编码的图像数据
            file_path: 保存文件的路径
            
        Returns:
            成功返回 True，失败返回 False
        """
        try:
            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # 解码并保存图像
            image_bytes = base64.b64decode(base64_data)
            
            with open(file_path, 'wb') as f:
                f.write(image_bytes)
            
            print(f"图像已保存到: {file_path}")
            return True
            
        except Exception as e:
            print(f"保存图像时发生错误: {str(e)}")
            return False

    @staticmethod
    def pil_to_base64(image: Image.Image, format: str = "PNG") -> Optional[str]:
        """
        将 PIL Image 转换为 base64 字符串
        
        Args:
            image: PIL Image 对象
            format: 图像格式 ("PNG", "JPEG", etc.)
            
        Returns:
            base64 编码的字符串，失败时返回 None
        """
        try:
            # 创建字节流
            buffer = io.BytesIO()
            
            # 保存图像到字节流
            image.save(buffer, format=format)
            
            # 获取字节数据并编码为 base64
            image_bytes = buffer.getvalue()
            base64_string = base64.b64encode(image_bytes).decode('utf-8')
            
            return base64_string
            
        except Exception as e:
            print(f"转换 PIL Image 到 base64 时发生错误: {str(e)}")
            return None

    @staticmethod
    def resize_image(base64_data: str, max_width: int, max_height: int) -> Optional[str]:
        """
        调整图像大小并返回 base64 数据
        
        Args:
            base64_data: 原始 base64 图像数据
            max_width: 最大宽度
            max_height: 最大高度
            
        Returns:
            调整大小后的 base64 图像数据，失败时返回 None
        """
        try:
            # 转换为 PIL Image
            image = ImageUtils.base64_to_pil_image(base64_data)
            if not image:
                return None
            
            # 计算新尺寸（保持宽高比）
            original_width, original_height = image.size
            ratio = min(max_width / original_width, max_height / original_height)
            
            if ratio < 1:  # 只在需要缩小时才调整
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                
                # 调整大小
                resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 转换回 base64
                return ImageUtils.pil_to_base64(resized_image)
            else:
                # 不需要调整，返回原数据
                return base64_data
                
        except Exception as e:
            print(f"调整图像大小时发生错误: {str(e)}")
            return None

    @staticmethod
    def create_thumbnail(base64_data: str, size: tuple = (200, 200)) -> Optional[str]:
        """
        创建缩略图
        
        Args:
            base64_data: 原始 base64 图像数据
            size: 缩略图尺寸 (width, height)
            
        Returns:
            缩略图的 base64 数据，失败时返回 None
        """
        try:
            # 转换为 PIL Image
            image = ImageUtils.base64_to_pil_image(base64_data)
            if not image:
                return None
            
            # 创建缩略图
            image.thumbnail(size, Image.Resampling.LANCZOS)
            
            # 转换回 base64
            return ImageUtils.pil_to_base64(image)
            
        except Exception as e:
            print(f"创建缩略图时发生错误: {str(e)}")
            return None

    def test_api_connection(self) -> bool:
        """
        测试 API 连接
        
        Returns:
            连接成功返回 True，失败返回 False
        """
        try:
            # 发送一个简单的测试请求
            test_payload = {
                "model": "dall-e-3",
                "prompt": "test",
                "n": 1,
                "size": "1024x1024"
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=test_payload,
                timeout=30  # 测试连接也增加超时时间
            )
            
            # 检查是否有有效响应（即使是错误响应也说明连接正常）
            return response.status_code in [200, 400, 401, 429]
            
        except Exception as e:
            print(f"API 连接测试失败: {str(e)}")
            return False

    @staticmethod
    def get_image_info(base64_data: str) -> dict:
        """
        获取图像信息
        
        Args:
            base64_data: base64 图像数据
            
        Returns:
            包含图像信息的字典
        """
        try:
            image = ImageUtils.base64_to_pil_image(base64_data)
            if not image:
                return {"error": "无法解析图像"}
            
            return {
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "format": image.format,
                "size_bytes": len(base64.b64decode(base64_data))
            }
            
        except Exception as e:
            return {"error": f"获取图像信息失败: {str(e)}"}


# 示例使用
if __name__ == "__main__":
    # 创建工具实例
    utils = ImageUtils()
    
    # 测试 API 连接
    print("测试 API 连接...")
    if utils.test_api_connection():
        print("✅ API 连接正常")
    else:
        print("❌ API 连接失败，请检查网络和 API Key")
    
    # 生成测试图像（如果有有效的 API Key）
    if utils.api_key != 'your-api-key-here':
        print("\n生成测试图像...")
        result = utils.generate_image("一只可爱的小猫")
        if result:
            print("✅ 图像生成成功")
            
            # 保存测试图像
            if ImageUtils.save_base64_image(result, "test_image.png"):
                print("✅ 图像保存成功")
            else:
                print("❌ 图像保存失败")
        else:
            print("❌ 图像生成失败")
    else:
        print("\n⚠️ 请设置有效的 API Key 以测试图像生成功能") 