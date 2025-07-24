# -*- coding: utf-8 -*-
"""
主窗口界面
使用 CustomTkinter 构建的现代化主窗口
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional

from utils.config_manager import config_manager
from ui.components import (
    HeaderFrame, ModernFrame, CustomTextBox, CustomEntry,
    NumberSlider, RatioSwitchSelector, ModelSwitchSelector, ProgressFrame, ImageDisplayFrame
)
from ui.widgets import GenerationManager


class MainWindow(ctk.CTk):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 设置外观模式和颜色主题
        ctk.set_appearance_mode("dark")  # 可选: "light", "dark", "system"
        ctk.set_default_color_theme("blue")  # 可选: "blue", "green", "dark-blue"
        
        # 初始化变量
        self.generation_manager = None
        self.is_generating = False
        
        # 设置窗口
        self.setup_window()
        
        # 创建UI
        self.create_widgets()
        
        # 设置事件绑定
        self.setup_bindings()
        
        # 加载配置
        self.load_settings()
    
    def setup_window(self):
        """设置窗口属性"""
        self.title("AI Image Generator - CustomTkinter Version")
        self.geometry("1000x800")
        self.minsize(800, 600)
        
        # 设置窗口图标
        import os
        import tkinter as tk
        icon_set = False
        
        # 方法1：尝试使用ICO文件
        try:
            logo_path = os.path.abspath("assets/logo.ico")
            if os.path.exists(logo_path):
                self.iconbitmap(logo_path)
                icon_set = True
        except Exception:
            pass
        
        # 方法2：如果ICO失败，尝试使用PNG文件
        if not icon_set:
            try:
                icon_png_path = os.path.abspath("assets/icon.png")
                if os.path.exists(icon_png_path):
                    # 加载PNG作为PhotoImage
                    icon_image = tk.PhotoImage(file=icon_png_path)
                    self.iconphoto(True, icon_image)
                    # 保存引用防止垃圾回收
                    self._icon_image = icon_image
                    icon_set = True
            except Exception:
                pass
        
        # 方法3：备用图标
        if not icon_set:
            try:
                icon_path = os.path.abspath("assets/icon.ico")
                if os.path.exists(icon_path):
                    self.iconbitmap(icon_path)
            except Exception:
                pass
        
        # 配置网格权重
        self.grid_rowconfigure(0, weight=0)  # 头部固定
        self.grid_rowconfigure(1, weight=0)  # API设置固定
        self.grid_rowconfigure(2, weight=0)  # 输入区域固定
        self.grid_rowconfigure(3, weight=0)  # 控制区域固定
        self.grid_rowconfigure(4, weight=0)  # 进度区域固定
        self.grid_rowconfigure(5, weight=1)  # 图像区域自适应
        self.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
        """创建界面组件"""
        # 头部区域
        self.header = HeaderFrame(
            self,
            title="AI 图像生成器",
            subtitle="轻量级 CustomTkinter 版本"
        )
        self.header.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="ew")
        
        # API设置区域
        self.api_frame = self.create_api_section()
        self.api_frame.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        
        # 输入区域
        self.input_frame = self.create_input_section()
        self.input_frame.grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        
        # 控制区域
        self.control_frame = self.create_control_section()
        self.control_frame.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        
        # 进度区域
        self.progress_frame = ProgressFrame(self)
        self.progress_frame.grid(row=4, column=0, padx=15, pady=5, sticky="ew")
        
        # 图像显示区域
        self.image_frame = self.create_image_section()
        self.image_frame.grid(row=5, column=0, padx=15, pady=(5, 15), sticky="nsew")
    
    def create_api_section(self) -> ModernFrame:
        """创建API设置区域"""
        frame = ModernFrame(self)
        
        # 标题
        title_label = ctk.CTkLabel(
            frame,
            text="🔑 API Settings",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 10), sticky="w")
        
        # API Key 输入
        api_key_label = ctk.CTkLabel(frame, text="API Key:", width=80)
        api_key_label.grid(row=1, column=0, padx=(15, 5), pady=5, sticky="w")
        
        self.api_key_entry = CustomEntry(
            frame,
            placeholder="Enter your API Key",
            show_password=True,
            width=400
        )
        self.api_key_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # 显示/隐藏密码按钮
        self.toggle_password_btn = ctk.CTkButton(
            frame,
            text="👁 Show",
            width=80,
            command=self.toggle_password_visibility
        )
        self.toggle_password_btn.grid(row=1, column=2, padx=(5, 15), pady=5)
        
        # API URL 输入
        api_url_label = ctk.CTkLabel(frame, text="API URL:", width=80)
        api_url_label.grid(row=2, column=0, padx=(15, 5), pady=5, sticky="w")
        
        self.api_url_entry = CustomEntry(
            frame,
            placeholder="https://api.apicore.ai/v1/images/generations",
            width=400
        )
        self.api_url_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # 保存按钮
        save_btn = ctk.CTkButton(
            frame,
            text="💾 Save",
            width=80,
            command=self.save_api_settings
        )
        save_btn.grid(row=2, column=2, padx=(5, 15), pady=5)
        
        # 配置网格权重
        frame.grid_columnconfigure(1, weight=1)
        
        return frame
    
    def create_input_section(self) -> ModernFrame:
        """创建输入区域"""
        frame = ModernFrame(self)
        
        # 标题
        title_label = ctk.CTkLabel(
            frame,
            text="📝 Describe the image you want to generate",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")
        
        # 文本输入框
        self.prompt_textbox = CustomTextBox(
            frame,
            placeholder="Enter image description, e.g.: A cute cat playing in a garden, sunny weather, high resolution..."
        )
        self.prompt_textbox.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        # 配置网格权重
        frame.grid_columnconfigure(0, weight=1)
        
        return frame
    
    def create_control_section(self) -> ModernFrame:
        """创建控制区域"""
        frame = ModernFrame(self)
        
        # 配置网格权重
        frame.grid_columnconfigure(3, weight=1)
        
        # 数量滑动器
        self.number_slider = NumberSlider(
            frame,
            title="生成数量",
            min_val=1,
            max_val=5,
            default_val=3,
            width=150
        )
        self.number_slider.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        # 比例选择器
        self.ratio_selector = RatioSwitchSelector(frame, width=150)
        self.ratio_selector.grid(row=0, column=1, padx=15, pady=15, sticky="w")
        
        # 模型选择器
        self.model_selector = ModelSwitchSelector(frame, width=150)
        self.model_selector.grid(row=0, column=2, padx=15, pady=15, sticky="w")
        
        # 生成按钮 - 视觉核心，正方形设计
        self.generate_btn = ctk.CTkButton(
            frame,
            text="🚀\nGenerate",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=80,
            width=80,
            fg_color=("#2563eb", "#1d4ed8"),
            hover_color=("#1d4ed8", "#1e3a8a"),
            corner_radius=12,
            border_width=2,
            border_color=("#1d4ed8", "#1e3a8a"),
            command=self.start_generation
        )
        self.generate_btn.grid(row=0, column=3, padx=15, pady=15, sticky="e")
        
        return frame
    
    def create_image_section(self) -> ImageDisplayFrame:
        """创建图像显示区域"""
        # 创建容器框架
        container = ModernFrame(self)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # 标题
        title_label = ctk.CTkLabel(
            container,
            text="🖼️ Generated Images",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        # 图像显示区域
        self.image_display = ImageDisplayFrame(container, height=300)
        self.image_display.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="nsew")
        
        return container
    
    def setup_bindings(self):
        """设置事件绑定"""
        # 窗口关闭事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_settings(self):
        """加载已保存的设置"""
        # 加载API设置
        api_key = config_manager.get_api_key()
        api_url = config_manager.get_api_url()
        
        if api_key:
            self.api_key_entry.delete(0, "end")
            self.api_key_entry.insert(0, api_key)
        
        if api_url:
            self.api_url_entry.delete(0, "end")
            self.api_url_entry.insert(0, api_url)
    
    def toggle_password_visibility(self):
        """切换密码可见性"""
        current_show = self.api_key_entry.cget("show")
        if current_show == "*":
            self.api_key_entry.configure(show="")
            self.toggle_password_btn.configure(text="🙈 Hide")
        else:
            self.api_key_entry.configure(show="*")
            self.toggle_password_btn.configure(text="👁 Show")
    
    def save_api_settings(self):
        """保存API设置"""
        # 获取输入值
        api_key = self.api_key_entry.get().strip()
        api_url = self.api_url_entry.get().strip()
        
        # 保存配置
        self.config_manager.set('api_key', api_key)
        self.config_manager.set('api_url', api_url)
        
        # 显示成功消息
        messagebox.showinfo("Success", "API settings saved successfully")
    
    def start_generation(self):
        """开始生成图片"""
        if self.is_generating:
            return
        
        # 获取输入内容
        prompt = self.prompt_textbox.get_text()
        if not prompt.strip():
            messagebox.showwarning("Input Error", "Please enter image description")
            return
        
        # 检查API Key
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showwarning("输入错误", "请输入 API Key")
            return
        
        # 获取参数
        num_images = self.number_slider.get_value()
        size = self.ratio_selector.get_current_key()
        model = self.model_selector.get_current_key()
        
        # 清除之前的图片
        self.image_display.clear_images()
        
        # 更新界面状态
        self.is_generating = True
        self.generate_btn.configure(
            state="disabled", 
            text="⏳\nGenerating...",
            fg_color=("gray70", "gray40"),
            hover_color=("gray70", "gray40")
        )
        self.progress_frame.set_status(f"🔄 正在生成 {num_images} 张图片...")
        self.progress_frame.start_indeterminate()
        
        # 创建生成管理器
        self.generation_manager = GenerationManager(
            self,
            progress_callback=self.on_generation_progress,
            complete_callback=self.on_image_complete,
            error_callback=self.on_generation_error,
            finished_callback=self.on_generation_complete
        )
        
        # 开始生成
        self.generation_manager.start_generation(prompt, num_images, api_key, size, model)
    
    def on_generation_progress(self, progress: float):
        """生成进度回调"""
        self.progress_frame.set_progress(progress)
    
    def on_image_complete(self, index: int, image_data: str):
        """图像生成完成回调"""
        try:
            self.image_display.add_image(image_data, index)
        except Exception as e:
            messagebox.showwarning("显示错误", f"无法显示第 {index+1} 张图片: {str(e)}")
    
    def on_generation_error(self, error_message: str):
        """生成错误回调"""
        messagebox.showerror("生成错误", error_message)
    
    def on_generation_complete(self):
        """所有生成完成"""
        self.is_generating = False
        self.generate_btn.configure(
            state="normal", 
            text="🚀\nGenerate",
            fg_color=("#2563eb", "#1d4ed8"),
            hover_color=("#1d4ed8", "#1e3a8a")
        )
        self.progress_frame.stop_indeterminate()
        self.progress_frame.set_status(f"✅ 完成！共生成 {self.image_display.get_image_count()} 张图片")
    
    def on_closing(self):
        """窗口关闭事件"""
        self.destroy()


# 应用程序入口点
def main():
    """主函数"""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main() 