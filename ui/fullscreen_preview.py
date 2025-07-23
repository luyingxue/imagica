# -*- coding: utf-8 -*-
"""
全屏图片预览窗口
提供沉浸式的全屏图片查看体验
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QFileDialog, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QFont, QKeySequence, QCursor

from utils.image_utils import ImageUtils
from utils.config_manager import config_manager
import uuid
import os
from datetime import datetime


class FullScreenPreview(QWidget):
    """全屏图片预览窗口"""
    
    def __init__(self, image_data: str, image_index: int, parent=None):
        super().__init__(parent)
        self.image_data = image_data
        self.image_index = image_index
        self.original_pixmap = None
        self.scale_factor = 1.0
        
        self.setup_ui()
        self.load_image()
    
    def setup_ui(self):
        """设置用户界面"""
        # 设置为全屏无边框窗口
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        # 设置黑色背景
        self.setStyleSheet("""
            QWidget {
                background-color: #000000;
            }
        """)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建顶部控制栏
        self.create_top_bar()
        main_layout.addWidget(self.top_bar)
        
        # 创建图片显示区域
        self.create_image_area()
        main_layout.addWidget(self.image_frame, 1)
        
        # 创建底部控制栏
        self.create_bottom_bar()
        main_layout.addWidget(self.bottom_bar)
        
        # 设置鼠标跟踪
        self.setMouseTracking(True)
        
        # 隐藏控制栏的定时器
        self.hide_timer = None
    
    def create_top_bar(self):
        """创建顶部控制栏"""
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(60)
        self.top_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 0, 0, 180),
                    stop:1 rgba(0, 0, 0, 0));
                border: none;
            }
        """)
        
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # 标题
        title_label = QLabel(f"图片预览 #{self.image_index + 1}")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
        """)
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # 关闭按钮
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 20);
                color: white;
                border: 2px solid rgba(255, 255, 255, 30);
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 100);
                border-color: rgba(255, 255, 255, 60);
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
    
    def create_image_area(self):
        """创建图片显示区域"""
        self.image_frame = QFrame()
        self.image_frame.setStyleSheet("background: transparent;")
        
        frame_layout = QVBoxLayout(self.image_frame)
        frame_layout.setContentsMargins(50, 20, 50, 20)
        
        # 保存成功提示标签（初始隐藏）
        self.save_success_label = QLabel("💾 图片保存成功！")
        self.save_success_label.setAlignment(Qt.AlignCenter)
        self.save_success_label.setStyleSheet("""
            QLabel {
                background-color: rgba(40, 167, 69, 200);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
            }
        """)
        self.save_success_label.hide()
        frame_layout.addWidget(self.save_success_label, 0, Qt.AlignTop | Qt.AlignCenter)
        
        # 图片标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background: transparent;")
        
        frame_layout.addWidget(self.image_label)
    
    def create_bottom_bar(self):
        """创建底部控制栏"""
        self.bottom_bar = QFrame()
        self.bottom_bar.setFixedHeight(80)
        self.bottom_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 0, 0, 0),
                    stop:1 rgba(0, 0, 0, 180));
                border: none;
            }
        """)
        
        layout = QHBoxLayout(self.bottom_bar)
        layout.setContentsMargins(50, 15, 50, 15)
        
        # 缩放控制
        zoom_out_btn = self.create_control_button("🔍-", "缩小")
        zoom_out_btn.clicked.connect(self.zoom_out)
        layout.addWidget(zoom_out_btn)
        
        zoom_reset_btn = self.create_control_button("⌂", "适应屏幕")
        zoom_reset_btn.clicked.connect(self.reset_zoom)
        layout.addWidget(zoom_reset_btn)
        
        zoom_in_btn = self.create_control_button("🔍+", "放大")
        zoom_in_btn.clicked.connect(self.zoom_in)
        layout.addWidget(zoom_in_btn)
        
        layout.addStretch()
        
        # 缩放比例显示
        self.scale_label = QLabel("100%")
        self.scale_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                padding: 10px;
            }
        """)
        layout.addWidget(self.scale_label)
        
        layout.addStretch()
        
        # 保存按钮
        save_btn = self.create_control_button("💾", "保存图片")
        save_btn.clicked.connect(self.save_image)
        layout.addWidget(save_btn)
    
    def create_control_button(self, text: str, tooltip: str) -> QPushButton:
        """创建控制按钮"""
        btn = QPushButton(text)
        btn.setFixedSize(50, 50)
        btn.setToolTip(tooltip)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 20);
                color: white;
                border: 2px solid rgba(255, 255, 255, 30);
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 40);
                border-color: rgba(255, 255, 255, 60);

            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 60);
            }
        """)
        return btn
    
    def load_image(self):
        """加载并显示图片"""
        try:
            # 将 base64 数据转换为 QPixmap
            self.original_pixmap = ImageUtils.base64_to_pixmap(self.image_data)
            
            if self.original_pixmap:
                self.reset_zoom()
            else:
                self.show_error("无法加载图片数据")
                
        except Exception as e:
            self.show_error(f"图片加载失败: {str(e)}")
    
    def display_image(self):
        """显示图片"""
        if not self.original_pixmap:
            return
        
        try:
            # 计算缩放后的尺寸
            scaled_size = self.original_pixmap.size() * self.scale_factor
            
            # 获取可用显示区域
            available_size = self.image_frame.size()
            available_size.setHeight(available_size.height() - 40)  # 减去边距
            available_size.setWidth(available_size.width() - 100)   # 减去边距
            
            # 如果缩放后的图片超出屏幕，进行适配
            if (scaled_size.width() > available_size.width() or 
                scaled_size.height() > available_size.height()):
                
                scaled_pixmap = self.original_pixmap.scaled(
                    scaled_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            else:
                scaled_pixmap = self.original_pixmap.scaled(
                    scaled_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            
            self.image_label.setPixmap(scaled_pixmap)
            
            # 更新缩放比例显示
            self.scale_label.setText(f"{int(self.scale_factor * 100)}%")
            
        except Exception as e:
            self.show_error(f"图片显示失败: {str(e)}")
    
    def zoom_in(self):
        """放大图片"""
        self.scale_factor = min(self.scale_factor * 1.25, 5.0)
        self.display_image()
    
    def zoom_out(self):
        """缩小图片"""
        self.scale_factor = max(self.scale_factor * 0.8, 0.1)
        self.display_image()
    
    def reset_zoom(self):
        """重置缩放到适应屏幕"""
        if not self.original_pixmap:
            return
        
        # 获取可用显示区域
        available_size = self.image_frame.size()
        available_size.setHeight(available_size.height() - 40)
        available_size.setWidth(available_size.width() - 100)
        
        # 计算适应屏幕的缩放比例
        image_size = self.original_pixmap.size()
        scale_w = available_size.width() / image_size.width()
        scale_h = available_size.height() / image_size.height()
        
        self.scale_factor = min(scale_w, scale_h, 1.0)  # 不放大
        self.display_image()
    
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
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存图片",
                os.path.join(last_save_dir, filename),
                "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
            )
            
            if file_path:
                # 保存图片
                success = ImageUtils.save_base64_image(self.image_data, file_path)
                
                if success:
                    # 记住保存目录
                    save_dir = os.path.dirname(file_path)
                    config_manager.config['last_save_dir'] = save_dir
                    config_manager.save_config()
                    
                    # 在状态栏显示保存成功信息（如果有的话）
                    print(f"💾 图片已保存: {os.path.basename(file_path)}")
                    # 在标题栏显示已保存状态
                    self.setWindowTitle(f"全屏预览 - 已保存")
                    self.save_success_label.show()
                    QTimer.singleShot(3000, self.save_success_label.hide) # 3秒后隐藏
                else:
                    QMessageBox.warning(self, "保存失败", "无法保存图片到指定位置")
                    
        except Exception as e:
            QMessageBox.warning(self, "保存错误", f"保存图片时发生错误:\n{str(e)}")
    
    def show_error(self, message: str):
        """显示错误信息"""
        self.image_label.setText(f"❌ {message}")
        self.image_label.setStyleSheet("""
            QLabel {
                color: #ff6b6b;
                background: transparent;
                font-size: 18px;
                padding: 50px;
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
        elif event.key() == Qt.Key_F or event.key() == Qt.Key_F11:
            # F 键或 F11 切换全屏（这里已经是全屏了）
            pass
        else:
            super().keyPressEvent(event)
    
    def wheelEvent(self, event):
        """鼠标滚轮事件"""
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            # 可以添加拖拽功能
            pass
        elif event.button() == Qt.RightButton:
            # 右键关闭
            self.close()
        super().mousePressEvent(event)
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        if self.original_pixmap:
            # 重新计算适应大小
            self.reset_zoom()
    
    def showEvent(self, event):
        """窗口显示事件"""
        super().showEvent(event)
        # 确保窗口在最前面
        self.raise_()
        self.activateWindow() 