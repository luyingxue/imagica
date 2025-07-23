# -*- coding: utf-8 -*-
"""
图片预览窗口
提供图片的放大预览和操作功能
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QFileDialog, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon

from utils.image_utils import ImageUtils
from utils.config_manager import config_manager
import uuid
import os
from datetime import datetime
from PyQt5.QtCore import QTimer


class ImagePreviewWindow(QDialog):
    """图片预览窗口"""
    
    def __init__(self, image_data: str, image_index: int, parent=None):
        super().__init__(parent)
        self.image_data = image_data
        self.image_index = image_index
        self.original_pixmap = None
        
        self.setup_ui()
        self.load_image()

    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle(f"图片预览 - 第 {self.image_index + 1} 张")
        self.setModal(True)
        self.resize(800, 600)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 创建顶部工具栏
        self.create_toolbar()
        main_layout.addWidget(self.toolbar)
        
        # 创建图片显示区域
        self.create_image_area()
        main_layout.addWidget(self.image_frame, 1)  # 占据主要空间
        
        # 创建底部按钮栏
        self.create_bottom_buttons()
        main_layout.addWidget(self.button_frame)

    def create_toolbar(self):
        """创建顶部工具栏"""
        self.toolbar = QFrame()
        self.toolbar.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        
        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        # 标题
        title_label = QLabel(f"🖼️ 预览图片 #{self.image_index + 1}")
        title_label.setFont(QFont("", 12, QFont.Bold))
        toolbar_layout.addWidget(title_label)
        
        toolbar_layout.addStretch()
        
        # 缩放按钮
        self.zoom_in_btn = QPushButton("🔍+ 放大")
        self.zoom_in_btn.setStyleSheet(self.get_button_style("#28a745"))
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        toolbar_layout.addWidget(self.zoom_in_btn)
        
        self.zoom_out_btn = QPushButton("🔍- 缩小")
        self.zoom_out_btn.setStyleSheet(self.get_button_style("#6c757d"))
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        toolbar_layout.addWidget(self.zoom_out_btn)
        
        # 添加适应屏幕按钮
        self.fit_screen_btn = QPushButton("⌂ 适应屏幕")
        self.fit_screen_btn.setStyleSheet(self.get_button_style("#17a2b8"))
        self.fit_screen_btn.clicked.connect(self.reset_zoom)
        toolbar_layout.addWidget(self.fit_screen_btn)
        
        # 全屏按钮
        self.fullscreen_btn = QPushButton("⛶ 全屏")
        self.fullscreen_btn.setStyleSheet(self.get_button_style("#9b59b6"))
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        toolbar_layout.addWidget(self.fullscreen_btn)

    def create_image_area(self):
        """创建图片显示区域"""
        self.image_frame = QFrame()
        self.image_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 5px;
            }
        """)
        
        frame_layout = QVBoxLayout(self.image_frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        
        # 滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f8f9fa;
            }
        """)
        
        # 图片标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(200, 200)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 3px;
            }
        """)
        
        self.scroll_area.setWidget(self.image_label)
        frame_layout.addWidget(self.scroll_area)

    def create_bottom_buttons(self):
        """创建底部按钮栏"""
        self.button_frame = QFrame()
        self.button_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        
        button_layout = QHBoxLayout(self.button_frame)
        button_layout.setContentsMargins(10, 5, 10, 5)
        
        # 保存按钮
        self.save_btn = QPushButton("💾 保存图片")
        self.save_btn.setStyleSheet(self.get_button_style("#007bff"))
        self.save_btn.clicked.connect(self.save_image)
        button_layout.addWidget(self.save_btn)
        
        button_layout.addStretch()
        
        # 关闭按钮
        self.close_btn = QPushButton("❌ 关闭")
        self.close_btn.setStyleSheet(self.get_button_style("#6c757d"))
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

    def get_button_style(self, color: str) -> str:
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 11px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}bb;
            }}
        """

    def load_image(self):
        """加载并显示图片"""
        try:
            # 将 base64 数据转换为 QPixmap
            self.original_pixmap = ImageUtils.base64_to_pixmap(self.image_data)
            
            if self.original_pixmap:
                # 初始显示时适应窗口大小
                self.display_image()
            else:
                self.show_error("无法加载图片数据")
                
        except Exception as e:
            self.show_error(f"图片加载失败: {str(e)}")

    def display_image(self, scale_factor: float = None):
        """显示图片"""
        if not self.original_pixmap:
            return
        
        try:
            if scale_factor is None:
                # 自动计算适应屏幕的缩放比例
                available_size = self.scroll_area.size()
                available_width = available_size.width() - 20
                available_height = available_size.height() - 20
                
                image_size = self.original_pixmap.size()
                image_width = image_size.width()
                image_height = image_size.height()
                
                if image_width > 0 and image_height > 0:
                    scale_w = available_width / image_width
                    scale_h = available_height / image_height
                    scale_factor = min(scale_w, scale_h, 1.0)  # 不超过原始大小
                else:
                    scale_factor = 1.0
            
            # 按比例缩放
            original_size = self.original_pixmap.size()
            new_width = int(original_size.width() * scale_factor)
            new_height = int(original_size.height() * scale_factor)
            scaled_pixmap = self.original_pixmap.scaled(
                new_width, new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.resize(scaled_pixmap.size())
            
        except Exception as e:
            self.show_error(f"图片显示失败: {str(e)}")

    def zoom_in(self):
        """放大图片"""
        try:
            current_size = self.image_label.size()
            original_size = self.original_pixmap.size()
            current_scale = current_size.width() / original_size.width()
            new_scale = min(current_scale * 1.25, 5.0)  # 最大放大5倍
            self.display_image(new_scale)
        except Exception as e:
            self.show_error(f"放大失败: {str(e)}")

    def zoom_out(self):
        """缩小图片"""
        try:
            current_size = self.image_label.size()
            original_size = self.original_pixmap.size()
            current_scale = current_size.width() / original_size.width()
            new_scale = max(current_scale * 0.8, 0.1)  # 最小缩小到0.1倍
            self.display_image(new_scale)
        except Exception as e:
            self.show_error(f"缩小失败: {str(e)}")

    def reset_zoom(self):
        """重置缩放到适应屏幕"""
        try:
            if not self.original_pixmap:
                return
            
            # 获取滚动区域的可用空间
            available_size = self.scroll_area.size()
            available_width = available_size.width() - 20  # 减去边距和滚动条空间
            available_height = available_size.height() - 20
            
            # 获取原图尺寸
            image_size = self.original_pixmap.size()
            image_width = image_size.width()
            image_height = image_size.height()
            
            # 计算缩放比例，确保图片完全显示在可用空间内
            scale_w = available_width / image_width if image_width > 0 else 1.0
            scale_h = available_height / image_height if image_height > 0 else 1.0
            
            # 选择较小的缩放比例，确保图片完全显示
            scale_factor = min(scale_w, scale_h, 1.0)  # 不超过原始大小
            
            # 应用缩放
            self.display_image(scale_factor)
            
        except Exception as e:
            self.show_error(f"适应屏幕失败: {str(e)}")
    
    def toggle_fullscreen(self):
        """切换全屏模式"""
        try:
            from ui.fullscreen_preview import FullScreenPreview
            fullscreen_window = FullScreenPreview(self.image_data, self.image_index, self)
            fullscreen_window.show()
        except Exception as e:
            QMessageBox.warning(self, "全屏预览错误", f"无法打开全屏预览: {str(e)}")

    def save_image(self):
        """保存图片"""
        try:
            # 获取上次保存的目录
            last_save_dir = config_manager.config.get('last_save_dir', '')
            if not last_save_dir or not os.path.exists(last_save_dir):
                last_save_dir = os.path.expanduser('~/Pictures')
            
            # 生成带随机数的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = str(uuid.uuid4())[:8]
            filename = f"ai_image_{self.image_index + 1}_{timestamp}_{random_suffix}.png"
            
            # 打开文件保存对话框
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存图片",
                os.path.join(last_save_dir, filename),
                "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
            )
            
            if file_path:
                # 使用工具类保存图片
                success = ImageUtils.save_base64_image(self.image_data, file_path)
                
                if success:
                    # 记住保存目录
                    save_dir = os.path.dirname(file_path)
                    config_manager.config['last_save_dir'] = save_dir
                    config_manager.save_config()
                    
                    # 在状态栏显示保存成功信息（如果有的话）
                    print(f"💾 图片已保存: {os.path.basename(file_path)}")
                    # 在标题栏显示已保存状态
                    self.setWindowTitle(f"图片预览 - 已保存 ✅")
                    # 显示保存成功消息框
                    QMessageBox.information(self, "保存成功", f"图片已成功保存到:\n{os.path.basename(file_path)}")
                else:
                    QMessageBox.warning(self, "保存失败", "无法保存图片到指定位置")
                    
        except Exception as e:
            QMessageBox.warning(self, "保存错误", f"保存图片时发生错误:\n{str(e)}")

    def show_error(self, message: str):
        """显示错误信息"""
        self.image_label.setText(f"❌ {message}")
        self.image_label.setStyleSheet("""
            QLabel {
                color: #dc3545;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 3px;
                padding: 20px;
                font-size: 14px;
            }
        """)

    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
            self.zoom_in()
        elif event.key() == Qt.Key_Minus:
            self.zoom_out()
        elif event.key() == Qt.Key_0:
            self.reset_zoom()
        elif event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save_image()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """窗口关闭事件"""
        event.accept()
    
    def showEvent(self, event):
        """窗口显示事件"""
        super().showEvent(event)
        # 窗口显示后重新应用适应屏幕缩放
        if self.original_pixmap:
            QTimer.singleShot(100, self.reset_zoom)  # 延迟100ms确保窗口完全显示 