# -*- coding: utf-8 -*-
"""
CustomTkinter UI组件模块
包含可重用的用户界面组件
"""

import customtkinter as ctk
from typing import Dict, Callable, Optional


class ModernFrame(ctk.CTkFrame):
    """现代化框架组件"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent, 
            corner_radius=12,
            **kwargs
        )


class HeaderFrame(ctk.CTkFrame):
    """头部框架组件"""
    
    def __init__(self, parent, title: str = "AI 图像生成器", subtitle: str = "基于 CustomTkinter 的现代化界面", **kwargs):
        super().__init__(
            parent,
            corner_radius=15,
            height=80,
            **kwargs
        )
        
        # 配置网格权重
        self.grid_columnconfigure(1, weight=1)
        
        # Logo 标签
        self.logo_label = ctk.CTkLabel(
            self,
            text="🎨",
            font=ctk.CTkFont(size=28)
        )
        self.logo_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        # 标题标签
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        
        # 副标题标签
        self.subtitle_label = ctk.CTkLabel(
            self,
            text=subtitle,
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.subtitle_label.grid(row=0, column=2, padx=15, pady=15, sticky="e")


class CustomTextBox(ctk.CTkTextbox):
    """自定义文本框"""
    
    def __init__(self, parent, placeholder: str = "", **kwargs):
        super().__init__(
            parent,
            corner_radius=10,
            height=100,
            **kwargs
        )
        self.placeholder = placeholder
        self.placeholder_active = False
        
        if placeholder:
            self.insert("1.0", placeholder)
            self.configure(text_color="gray60")
            self.placeholder_active = True
        
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        if self.placeholder_active:
            self.delete("1.0", "end")
            self.configure(text_color="white")
            self.placeholder_active = False
    
    def _on_focus_out(self, event):
        if not self.get("1.0", "end-1c").strip():
            self.insert("1.0", self.placeholder)
            self.configure(text_color="gray60")
            self.placeholder_active = True
    
    def get_text(self) -> str:
        """获取文本内容（不包括占位符）"""
        if self.placeholder_active:
            return ""
        return self.get("1.0", "end-1c").strip()


class CustomEntry(ctk.CTkEntry):
    """自定义输入框"""
    
    def __init__(self, parent, placeholder: str = "", show_password: bool = False, **kwargs):
        super().__init__(
            parent,
            placeholder_text=placeholder,
            corner_radius=8,
            height=35,
            **kwargs
        )
        if show_password:
            self.configure(show="*")


class NumberSlider(ctk.CTkFrame):
    """数字滑动器组件"""
    
    def __init__(self, parent, title: str, min_val: int = 1, max_val: int = 5, 
                 default_val: int = 3, callback: Callable = None, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self.callback = callback
        
        # 配置网格
        self.grid_columnconfigure(1, weight=1)
        
        # 标题
        self.title_label = ctk.CTkLabel(
            self,
            text=f"🔢 {title}",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # 数值显示
        self.value_label = ctk.CTkLabel(
            self,
            text=str(default_val),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=40,
            height=25,
            corner_radius=6,
            fg_color=("gray75", "gray25")
        )
        self.value_label.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="e")
        
        # 滑动条
        self.slider = ctk.CTkSlider(
            self,
            from_=min_val,
            to=max_val,
            number_of_steps=max_val - min_val,
            command=self._on_value_change
        )
        self.slider.set(default_val)
        self.slider.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
    
    def _on_value_change(self, value):
        """滑动条值改变回调"""
        int_value = int(value)
        self.value_label.configure(text=str(int_value))
        if self.callback:
            self.callback(int_value)
    
    def get_value(self) -> int:
        """获取当前值"""
        return int(self.slider.get())
    
    def set_value(self, value: int):
        """设置值"""
        self.slider.set(value)
        self.value_label.configure(text=str(value))


class OptionSelector(ctk.CTkFrame):
    """选项选择器组件"""
    
    def __init__(self, parent, title: str, options: Dict[str, str], 
                 default_key: str = None, callback: Callable = None, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self.options = options
        self.current_key = default_key or list(options.keys())[0]
        self.callback = callback
        self.buttons = []
        
        # 标题
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=len(options), padx=10, pady=(10, 5), sticky="w")
        
        # 选项按钮
        for i, (key, display_name) in enumerate(options.items()):
            btn = ctk.CTkButton(
                self,
                text=display_name,
                width=70,
                height=30,
                font=ctk.CTkFont(size=11),
                command=lambda k=key: self._select_option(k)
            )
            btn.grid(row=1, column=i, padx=5, pady=(0, 10), sticky="ew")
            self.buttons.append((key, btn))
        
        # 设置初始选择
        self._update_button_states()
    
    def _select_option(self, key: str):
        """选择选项"""
        self.current_key = key
        self._update_button_states()
        if self.callback:
            self.callback(key)
    
    def _update_button_states(self):
        """更新按钮状态"""
        for key, btn in self.buttons:
            if key == self.current_key:
                # 选中状态：蓝色背景，白色文字
                btn.configure(
                    fg_color=("#1f538d", "#14375e"),
                    text_color=("white", "white"),
                    border_width=2,
                    border_color=("#1f538d", "#14375e")
                )
            else:
                # 未选中状态：灰色背景，深色文字
                btn.configure(
                    fg_color=("gray80", "gray20"),
                    text_color=("gray30", "gray80"),
                    border_width=1,
                    border_color=("gray70", "gray30")
                )
    
    def get_current_key(self) -> str:
        """获取当前选择的key"""
        return self.current_key
    
    def get_current_value(self) -> str:
        """获取当前选择的显示名称"""
        return self.options[self.current_key]


class RatioSelector(OptionSelector):
    """比例选择器"""
    
    def __init__(self, parent, callback: Callable = None, **kwargs):
        options = {
            "1024x1536": "竖屏",
            "1536x1024": "横屏"
        }
        super().__init__(
            parent, 
            "📐 比例", 
            options, 
            "1024x1536", 
            callback,
            **kwargs
        )


class ModelSelector(OptionSelector):
    """模型选择器"""
    
    def __init__(self, parent, callback: Callable = None, **kwargs):
        options = {
            "sora_image": "Sora",
            "gpt-image-1": "GPT-4o"
        }
        super().__init__(
            parent, 
            "🤖 模型", 
            options, 
            "sora_image", 
            callback,
            **kwargs
        )


class ProgressFrame(ctk.CTkFrame):
    """进度显示框架"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        # 状态标签
        self.status_label = ctk.CTkLabel(
            self,
            text="📊 准备就绪",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.status_label.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")
        
        # 进度条
        self.progress_bar = ctk.CTkProgressBar(
            self,
            height=6,
            corner_radius=3
        )
        self.progress_bar.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)
        
        # 配置网格
        self.grid_columnconfigure(0, weight=1)
    
    def set_status(self, text: str):
        """设置状态文本"""
        self.status_label.configure(text=text)
    
    def set_progress(self, value: float):
        """设置进度值 (0.0 - 1.0)"""
        self.progress_bar.set(value)
    
    def start_indeterminate(self):
        """开始不确定进度模式"""
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
    
    def stop_indeterminate(self):
        """停止不确定进度模式"""
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")


class ImageDisplayFrame(ctk.CTkScrollableFrame):
    """图像显示框架"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            corner_radius=10,
            **kwargs
        )
        
        self.images = []  # 存储图像数据
        self.image_widgets = []  # 存储图像控件
        
        # 配置网格权重
        for i in range(3):  # 支持3列布局
            self.grid_columnconfigure(i, weight=1)
    
    def add_image(self, image_data: str, index: int):
        """添加图像"""
        from ui.widgets import ImageThumbnail
        
        try:
            # 计算网格位置
            row = index // 3
            col = index % 3
            
            # 创建图像缩略图
            thumbnail = ImageThumbnail(self, image_data, index)
            thumbnail.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            self.images.append(image_data)
            self.image_widgets.append(thumbnail)
            
        except Exception as e:
            print(f"添加图像失败: {str(e)}")
    
    def clear_images(self):
        """清除所有图像"""
        for widget in self.image_widgets:
            widget.destroy()
        
        self.images.clear()
        self.image_widgets.clear()
    
    def get_image_count(self) -> int:
        """获取图像数量"""
        return len(self.images) 


class SwitchSelector(ctk.CTkFrame):
    """通用开关选择器组件 - 适用于二选一场景"""
    
    def __init__(self, parent, title: str, option_off: str, option_on: str, 
                 key_off: str, key_on: str, default_on: bool = False, 
                 callback: Callable = None, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self.option_off = option_off  # 关闭状态的显示文本
        self.option_on = option_on    # 开启状态的显示文本
        self.key_off = key_off        # 关闭状态的值
        self.key_on = key_on          # 开启状态的值
        self.callback = callback
        
        # 配置网格
        self.grid_columnconfigure(0, weight=1)
        
        # 标题
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # 开关容器
        switch_container = ctk.CTkFrame(self, fg_color="transparent")
        switch_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        switch_container.grid_columnconfigure((0, 2), weight=1)
        
        # 左侧选项标签
        self.left_label = ctk.CTkLabel(
            switch_container,
            text=option_off,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#2563eb", "#60a5fa")  # 默认选中状态颜色
        )
        self.left_label.grid(row=0, column=0, padx=5, sticky="e")
        
        # 开关控件
        self.switch = ctk.CTkSwitch(
            switch_container,
            text="",
            width=50,
            command=self._on_switch_change,
            fg_color=("#cbd5e1", "#475569"),  # 未选中时的轨道颜色
            progress_color=("#2563eb", "#1d4ed8"),  # 选中时的颜色
            button_color=("white", "#f1f5f9"),  # 按钮颜色
            button_hover_color=("#e2e8f0", "#cbd5e1")  # 按钮悬停颜色
        )
        self.switch.grid(row=0, column=1, padx=10)
        
        # 右侧选项标签
        self.right_label = ctk.CTkLabel(
            switch_container,
            text=option_on,
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray40")  # 默认未选中状态颜色
        )
        self.right_label.grid(row=0, column=2, padx=5, sticky="w")
        
        # 设置默认状态
        if default_on:
            self.switch.select()
        
        # 更新标签状态
        self._update_labels()
    
    def _on_switch_change(self):
        """开关状态改变回调"""
        self._update_labels()
        if self.callback:
            self.callback(self.get_current_key())
    
    def _update_labels(self):
        """更新标签的视觉状态"""
        if self.switch.get():
            # 右侧选中
            self.left_label.configure(
                font=ctk.CTkFont(size=11),
                text_color=("gray60", "gray40")
            )
            self.right_label.configure(
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=("#2563eb", "#60a5fa")
            )
        else:
            # 左侧选中
            self.left_label.configure(
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=("#2563eb", "#60a5fa")
            )
            self.right_label.configure(
                font=ctk.CTkFont(size=11),
                text_color=("gray60", "gray40")
            )
    
    def get_current_key(self) -> str:
        """获取当前选择的key"""
        return self.key_on if self.switch.get() else self.key_off
    
    def get_current_value(self) -> str:
        """获取当前选择的显示名称"""
        return self.option_on if self.switch.get() else self.option_off
    
    def set_value(self, key: str):
        """设置当前值"""
        if key == self.key_on:
            self.switch.select()
        else:
            self.switch.deselect()
        self._update_labels()


class RatioSwitchSelector(SwitchSelector):
    """比例开关选择器"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            title="📐 Aspect Ratio",
            option_off="Portrait",
            option_on="Landscape", 
            key_off="1024x1536",
            key_on="1536x1024",
            default_on=False,
            **kwargs
        )


class ModelSwitchSelector(SwitchSelector):
    """模型开关选择器"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            title="🤖 AI Model",
            option_off="Sora",
            option_on="GPT-4o",
            key_off="sora_image", 
            key_on="gpt-image-1",
            default_on=False,
            **kwargs
        ) 