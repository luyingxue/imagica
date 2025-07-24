# -*- coding: utf-8 -*-
"""
CustomTkinter 自定义小部件模块
包含应用程序特定的复杂UI组件
"""

import os
import uuid
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, Toplevel
from typing import Optional

import customtkinter as ctk
from PIL import Image, ImageTk

from utils.image_utils import ImageUtils
from utils.config_manager import config_manager


class ImageThumbnail(ctk.CTkFrame):
    """图像缩略图组件"""
    
    def __init__(self, parent, image_data: str, index: int, **kwargs):
        super().__init__(
            parent,
            corner_radius=12,
            width=180,
            height=270,
            **kwargs
        )
        
        self.image_data = image_data
        self.index = index
        self.parent_window = parent
        
        # 创建图像标签
        self.image_label = ctk.CTkLabel(
            self,
            text="",
            width=160,
            height=240,
            corner_radius=8
        )
        self.image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # 加载并显示图像
        self.load_image()
        
        # 绑定事件
        self.image_label.bind("<Button-1>", self.on_click)
        self.image_label.bind("<Double-Button-1>", self.on_double_click)
        self.image_label.bind("<Button-3>", self.show_context_menu)
        
        # 配置网格权重
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def load_image(self):
        """加载并显示图像"""
        try:
            # 转换为CustomTkinter兼容的图像并缩放
            image = ImageUtils.base64_to_tk_image(self.image_data, (160, 240))
            if image:
                self.image_label.configure(image=image)
                # 保存引用防止垃圾回收
                self.image_label._image = image
            else:
                self.image_label.configure(text="Load Failed")
        except Exception as e:
            self.image_label.configure(text=f"Error: {str(e)}")
    
    def on_click(self, event):
        """单击事件 - 显示全屏预览"""
        self.show_fullscreen_preview()
    
    def on_double_click(self, event):
        """双击事件 - 不做任何操作，避免重复触发"""
        pass
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        try:
            # 创建上下文菜单
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(label="🖼️ 窗口预览", command=self.show_preview)
            context_menu.add_command(label="⛶ 全屏预览", command=self.show_fullscreen_preview)
            context_menu.add_separator()
            context_menu.add_command(label="💾 保存图片", command=self.save_image)
            
            # 显示菜单
            context_menu.tk_popup(event.x_root, event.y_root)
        except Exception as e:
            print(f"显示上下文菜单失败: {str(e)}")
    
    def show_preview(self):
        """显示图像预览窗口"""
        try:
            preview_window = ImagePreviewWindow(self.winfo_toplevel(), self.image_data, self.index)
            preview_window.focus()
        except Exception as e:
            messagebox.showerror("预览错误", f"无法显示预览: {str(e)}")
    
    def show_fullscreen_preview(self):
        """显示全屏图像预览"""
        try:
            fullscreen_window = FullScreenPreview(self.winfo_toplevel(), self.image_data, self.index)
            fullscreen_window.focus()
        except Exception as e:
            messagebox.showerror("预览错误", f"无法显示全屏预览: {str(e)}")
    
    def save_image(self):
        """保存图像到本地"""
        try:
            # 获取上次保存的目录
            last_save_dir = config_manager.config.get('last_save_dir', '')
            if not last_save_dir or not os.path.exists(last_save_dir):
                last_save_dir = os.path.expanduser('~/Pictures')
            
            # 生成带随机数的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = str(uuid.uuid4())[:8]
            filename = f"ai_image_{self.index + 1}_{timestamp}_{random_suffix}.png"
            
            file_path = filedialog.asksaveasfilename(
                title="保存图片",
                initialdir=last_save_dir,
                initialfile=filename,
                defaultextension=".png",
                filetypes=[("PNG 文件", "*.png"), ("JPEG 文件", "*.jpg"), ("所有文件", "*.*")]
            )
            
            if file_path:
                success = ImageUtils.save_base64_image(self.image_data, file_path)
                if success:
                    # 记住保存目录
                    save_dir = os.path.dirname(file_path)
                    config_manager.config['last_save_dir'] = save_dir
                    config_manager.save_config()
                    
                    messagebox.showinfo("保存成功", f"图片已保存: {os.path.basename(file_path)}")
                else:
                    messagebox.showerror("保存失败", "无法保存图片")
                    
        except Exception as e:
            messagebox.showerror("保存错误", f"保存错误：{str(e)}")


class ImagePreviewWindow(ctk.CTkToplevel):
    """图像预览窗口"""
    
    def __init__(self, parent, image_data: str, index: int, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.image_data = image_data
        self.index = index
        
        # 设置窗口属性
        self.title(f"AI Image Generator - Preview (Image {index + 1})")
        self.geometry("600x700")
        self.resizable(True, True)
        
        # 设置窗口图标
        try:
            if hasattr(parent, 'iconbitmap'):
                # 继承父窗口的图标
                self.iconbitmap(default=parent.iconbitmap())
        except:
            pass
        
        # 设置窗口居中
        self.center_window()
        
        # 创建UI
        self.create_widgets()
        
        # 使窗口模态
        self.transient(parent)
        self.grab_set()
    
    def center_window(self):
        """窗口居中"""
        self.update_idletasks()
        width = 600
        height = 700
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """创建控件"""
        # 图像显示区域
        self.image_label = ctk.CTkLabel(
            self,
            text="",
            width=550,
            height=550
        )
        self.image_label.pack(padx=20, pady=20, expand=True, fill="both")
        
        # 状态提示标签
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("green", "lightgreen"),
            height=20
        )
        self.status_label.pack(padx=20, pady=(0, 10))
        
        # 按钮框架
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(padx=20, pady=(0, 20), fill="x")
        
        # 保存按钮
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Image",
            command=self.save_image
        )
        save_btn.pack(side="left", padx=(10, 5), pady=10)
        
        # 关闭按钮
        close_btn = ctk.CTkButton(
            button_frame,
            text="❌ Close",
            command=self.destroy
        )
        close_btn.pack(side="right", padx=(5, 10), pady=10)
        
        # 加载图像
        self.load_image()
    
    def load_image(self):
        """加载图像"""
        try:
            # 对于CTkLabel，使用PhotoImage而不是CTkImage
            image = ImageUtils.base64_to_tk_image(self.image_data, (550, 550), use_ctk_image=False)
            if image:
                self.image_label.configure(image=image)
                self.image_label._image = image
            else:
                self.image_label.configure(text="Unable to load image")
        except Exception as e:
            self.image_label.configure(text=f"Load error: {str(e)}")
    
    def save_image(self):
        """保存图像"""
        try:
            # 临时释放模态状态，避免阻止保存对话框
            self.grab_release()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = str(uuid.uuid4())[:8]
            filename = f"ai_image_{self.index + 1}_{timestamp}_{random_suffix}.png"
            
            file_path = filedialog.asksaveasfilename(
                title="Save Image",
                initialfile=filename,
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]
            )
            
            # 恢复模态状态
            self.grab_set()
            
            if file_path:
                success = ImageUtils.save_base64_image(self.image_data, file_path)
                if success:
                    # 在界面显示成功信息
                    self.status_label.configure(
                        text=f"✅ Image saved: {os.path.basename(file_path)}",
                        text_color=("green", "lightgreen")
                    )
                    # 3秒后清除提示
                    self.after(3000, lambda: self.status_label.configure(text=""))
                else:
                    # 在界面显示错误信息
                    self.status_label.configure(
                        text="❌ Failed to save image",
                        text_color=("red", "lightcoral")
                    )
                    # 3秒后清除提示
                    self.after(3000, lambda: self.status_label.configure(text=""))
        except Exception as e:
            # 确保即使出错也恢复模态状态
            self.grab_set()
            # 在界面显示错误信息
            self.status_label.configure(
                text=f"❌ Save error: {str(e)}",
                text_color=("red", "lightcoral")
            )
            # 3秒后清除提示
            self.after(3000, lambda: self.status_label.configure(text=""))


class FullScreenPreview(ctk.CTkToplevel):
    """全屏图像预览"""
    
    def __init__(self, parent, image_data: str, index: int, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.image_data = image_data
        self.index = index
        self.scale_factor = 1.0
        
        # 设置全屏
        self.attributes("-fullscreen", True)
        self.attributes("-topmost", True)
        self.configure(fg_color="black")
        
        # 创建UI
        self.create_widgets()
        
        # 绑定键盘事件
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Button-3>", lambda e: self.destroy())  # 右键退出
        self.bind("<KeyPress>", self.on_key_press)
        self.focus_set()
    
    def create_widgets(self):
        """创建控件"""
        # 主容器，使用固定布局
        main_frame = tk.Frame(self, bg="black")
        main_frame.pack(fill="both", expand=True)
        
        # 图像显示区域 - 留出底部空间给控制按钮
        self.image_label = tk.Label(
            main_frame,
            bg="black",
            cursor="crosshair"
        )
        self.image_label.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        
        # 控制按钮框架 - 固定在底部
        control_frame = ctk.CTkFrame(main_frame, fg_color=("gray90", "gray20"), corner_radius=8, height=60, width=500)
        control_frame.place(relx=0.5, rely=1.0, anchor="s", y=-20)
        
        # 确保控制框架不会改变大小
        control_frame.pack_propagate(False)
        
        # 缩放按钮
        zoom_out_btn = ctk.CTkButton(
            control_frame,
            text="🔍-",
            width=40,
            height=30,
            command=self.zoom_out
        )
        zoom_out_btn.pack(side="left", padx=5, pady=15)
        
        zoom_in_btn = ctk.CTkButton(
            control_frame,
            text="🔍+",
            width=40,
            height=30,
            command=self.zoom_in
        )
        zoom_in_btn.pack(side="left", padx=5, pady=15)
        
        reset_btn = ctk.CTkButton(
            control_frame,
            text="⚡ Reset",
            width=60,
            height=30,
            command=self.reset_zoom
        )
        reset_btn.pack(side="left", padx=5, pady=15)
        
        # 保存按钮
        save_btn = ctk.CTkButton(
            control_frame,
            text="💾 Save",
            width=60,
            height=30,
            command=self.save_image
        )
        save_btn.pack(side="left", padx=10, pady=15)
        
        # 退出按钮
        exit_btn = ctk.CTkButton(
            control_frame,
            text="❌ Exit",
            width=60,
            height=30,
            command=self.destroy
        )
        exit_btn.pack(side="right", padx=5, pady=15)
        
        # 加载图像
        self.load_image()
    
    def load_image(self):
        """加载图像"""
        try:
            # 获取屏幕尺寸
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight() - 100  # 留出按钮空间
            
            # 转换图像 - 对于tk.Label使用PhotoImage
            pil_image = ImageUtils.base64_to_pil_image(self.image_data)
            if pil_image:
                # 计算适合屏幕的尺寸
                img_width, img_height = pil_image.size
                scale = min(screen_width / img_width, screen_height / img_height)
                
                new_width = int(img_width * scale * self.scale_factor)
                new_height = int(img_height * scale * self.scale_factor)
                
                # 调整图像大小
                resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 转换为PhotoImage - 适用于标准tkinter控件
                self.photo = ImageTk.PhotoImage(resized_image)
                self.image_label.configure(image=self.photo)
            else:
                self.image_label.configure(text="无法加载图像", fg="white", font=("Arial", 24))
        except Exception as e:
            self.image_label.configure(text=f"加载错误: {str(e)}", fg="white", font=("Arial", 24))
    
    def zoom_in(self):
        """放大"""
        self.scale_factor *= 1.2
        self.load_image()
    
    def zoom_out(self):
        """缩小"""
        self.scale_factor /= 1.2
        self.load_image()
    
    def reset_zoom(self):
        """重置缩放"""
        self.scale_factor = 1.0
        self.load_image()
    
    def on_key_press(self, event):
        """键盘事件处理"""
        if event.keysym == "plus" or event.keysym == "equal":
            self.zoom_in()
        elif event.keysym == "minus":
            self.zoom_out()
        elif event.keysym == "0":
            self.reset_zoom()
        elif event.char.lower() == "s":
            self.save_image()
    
    def save_image(self):
        """保存图像"""
        try:
            # 临时移除topmost属性，避免覆盖保存对话框
            self.attributes("-topmost", False)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = str(uuid.uuid4())[:8]
            filename = f"ai_image_{self.index + 1}_{timestamp}_{random_suffix}.png"
            
            file_path = filedialog.asksaveasfilename(
                title="Save Image",
                initialfile=filename,
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]
            )
            
            # 恢复topmost属性
            self.attributes("-topmost", True)
            
            if file_path:
                success = ImageUtils.save_base64_image(self.image_data, file_path)
                if success:
                    messagebox.showinfo("Success", f"Image saved: {os.path.basename(file_path)}")
                else:
                    messagebox.showerror("Error", "Failed to save image")
        except Exception as e:
            # 确保即使出错也恢复topmost属性
            self.attributes("-topmost", True)
            messagebox.showerror("Save Error", f"Save error: {str(e)}")


class GenerationManager:
    """图像生成管理器"""
    
    def __init__(self, parent_window, progress_callback=None, complete_callback=None, error_callback=None, finished_callback=None):
        self.parent_window = parent_window
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback
        self.error_callback = error_callback
        self.finished_callback = finished_callback
        self.completed_count = 0
        self.total_count = 0
        self.is_generating = False
    
    def start_generation(self, prompt: str, num_images: int, api_key: str, size: str, model: str):
        """开始图像生成"""
        if self.is_generating:
            return
        
        self.is_generating = True
        self.completed_count = 0
        self.total_count = num_images
        
        # 创建图像工具实例
        image_utils = ImageUtils(api_key)
        
        # 异步生成所有图像
        for i in range(num_images):
            image_utils.generate_image_async(
                prompt=prompt,
                size=size,
                model=model,
                callback=self._on_image_complete,
                index=i
            )
    
    def _on_image_complete(self, index: int, image_data: Optional[str]):
        """图像生成完成回调"""
        self.completed_count += 1
        
        if image_data:
            # 通知图像生成成功
            if self.complete_callback:
                self.complete_callback(index, image_data)
        else:
            # 通知错误
            if self.error_callback:
                self.error_callback(f"第 {index + 1} 张图片生成失败")
        
        # 更新进度
        if self.progress_callback:
            progress = self.completed_count / self.total_count
            self.progress_callback(progress)
        
        # 检查是否全部完成
        if self.completed_count >= self.total_count:
            self.is_generating = False
            # 调用完成回调
            if self.finished_callback:
                self.finished_callback() 