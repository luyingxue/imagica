# -*- coding: utf-8 -*-
"""
自定义小部件模块
包含应用程序特定的复杂UI组件
"""

import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List, Optional

from PyQt5.QtWidgets import (
    QLabel, QMenu, QAction, QFileDialog, QMessageBox,
    QProgressBar, QScrollArea, QGridLayout, QWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QFont, QCursor

from utils.image_utils import ImageUtils
from utils.config_manager import config_manager
from ui.image_preview import ImagePreviewWindow
from ui.fullscreen_preview import FullScreenPreview


class ImageGenerationThread(QThread):
    """图像生成线程"""
    progress_updated = pyqtSignal(int)  # 进度更新信号
    image_generated = pyqtSignal(int, str)  # 图像生成完成信号 (index, base64_data)
    generation_completed = pyqtSignal()  # 所有图像生成完成信号
    error_occurred = pyqtSignal(str)  # 错误信号

    def __init__(self, prompt: str, num_images: int, api_key: str, size: str = "1024x1536", model: str = "sora_image"):
        super().__init__()
        self.prompt = prompt
        self.num_images = num_images
        self.api_key = api_key
        self.size = size
        self.model = model
        self.image_utils = ImageUtils(api_key)

    def run(self):
        """运行图像生成任务"""
        try:
            # 根据图片数量动态调整线程数，最多使用5个线程
            max_workers = min(self.num_images, 5)
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 提交所有生成任务
                futures = {}
                for i in range(self.num_images):
                    future = executor.submit(self.image_utils.generate_image, self.prompt, self.size, self.model)
                    futures[future] = i

                # 使用 as_completed 来处理完成的任务，提高响应速度
                from concurrent.futures import as_completed
                completed = 0
                
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        image_index = futures[future]
                        
                        if result:
                            self.image_generated.emit(image_index, result)
                        
                        completed += 1
                        progress = int((completed / self.num_images) * 100)
                        self.progress_updated.emit(progress)
                        
                    except Exception as e:
                        image_index = futures[future]
                        self.error_occurred.emit(f"生成第 {image_index+1} 张图片时出错: {str(e)}")

                self.generation_completed.emit()

        except Exception as e:
            self.error_occurred.emit(f"图像生成失败: {str(e)}")


class ImageThumbnail(QLabel):
    """图片缩略图组件"""
    
    def __init__(self, image_data: str, index: int, parent=None):
        super().__init__(parent)
        self.image_data = image_data
        self.index = index
        self.parent_window = parent
        self.preview_window_open = False  # 防止重复打开窗口
        
        # 设置样式 - 2:3比例
        self.setFixedSize(200, 300)
        self.setStyleSheet("""
            QLabel {
                border: 2px solid rgba(148, 163, 184, 0.2);
                border-radius: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #f8fafc);
                padding: 6px;
            }
            QLabel:hover {
                border-color: #3b82f6;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #dbeafe, stop:1 #bfdbfe);
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)
        
        # 加载并显示图片
        self.load_image()
        
        # 设置右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def load_image(self):
        """加载并显示图片"""
        try:
            pixmap = ImageUtils.base64_to_pixmap(self.image_data)
            if pixmap:
                # 缩放图片以适应缩略图大小
                scaled_pixmap = pixmap.scaled(
                    self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.setPixmap(scaled_pixmap)
            else:
                self.setText("加载失败")
        except Exception as e:
            self.setText(f"错误: {str(e)}")

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            # 单击事件 - 不立即处理，等待可能的双击
            pass
        elif event.button() == Qt.RightButton:
            # 右键显示上下文菜单
            self.show_context_menu(event.pos())
        super().mousePressEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if event.button() == Qt.LeftButton:
            # 双击显示全屏预览窗口
            self.show_fullscreen_preview()
        super().mouseDoubleClickEvent(event)

    def show_fullscreen_preview(self):
        """显示全屏图片预览窗口"""
        # 防止重复打开窗口
        if self.preview_window_open:
            return
            
        try:
            self.preview_window_open = True
            fullscreen_window = FullScreenPreview(self.image_data, self.index, self.parent_window)
            # 保存窗口引用以便管理
            self.fullscreen_window = fullscreen_window
            # 使用定时器在一定时间后重置标志，允许再次打开
            QTimer.singleShot(1000, lambda: setattr(self, 'preview_window_open', False))
            fullscreen_window.show()
        except Exception as e:
            self.preview_window_open = False
            QMessageBox.warning(self.parent_window, "预览错误", f"无法显示全屏预览: {str(e)}")

    def show_preview(self):
        """显示图片预览窗口（保留原功能用于右键菜单）"""
        try:
            preview_window = ImagePreviewWindow(self.image_data, self.index, self)
            preview_window.exec_()
        except Exception as e:
            QMessageBox.warning(self, "预览错误", f"无法显示预览: {str(e)}")

    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)
        
        # 预览图片动作
        preview_action = QAction("🖼️ 窗口预览", self)
        preview_action.triggered.connect(self.show_preview)
        menu.addAction(preview_action)
        
        # 全屏预览动作
        fullscreen_action = QAction("⛶ 全屏预览", self)
        fullscreen_action.triggered.connect(self.show_fullscreen_preview)
        menu.addAction(fullscreen_action)
        
        menu.addSeparator()  # 添加分隔线
        
        # 保存图片动作
        save_action = QAction("💾 保存图片", self)
        save_action.triggered.connect(self.save_image)
        menu.addAction(save_action)
        
        # 显示菜单
        menu.exec_(self.mapToGlobal(position))

    def save_image(self):
        """保存图片到本地"""
        try:
            # 获取上次保存的目录
            last_save_dir = config_manager.config.get('last_save_dir', '')
            if not last_save_dir or not os.path.exists(last_save_dir):
                last_save_dir = os.path.expanduser('~/Pictures')
            
            # 生成带随机数的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = str(uuid.uuid4())[:8]
            filename = f"ai_image_{self.index + 1}_{timestamp}_{random_suffix}.png"
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "保存图片", 
                os.path.join(last_save_dir, filename),
                "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
            )
            
            if file_path:
                success = ImageUtils.save_base64_image(self.image_data, file_path)
                if success:
                    # 记住保存目录
                    save_dir = os.path.dirname(file_path)
                    config_manager.config['last_save_dir'] = save_dir
                    config_manager.save_config()
                    
                    # 显示保存成功消息
                    if hasattr(self.parent_window, 'show_save_success'):
                        self.parent_window.show_save_success(f"图片已保存: {os.path.basename(file_path)}")
                    else:
                        QMessageBox.information(self, "保存成功", f"图片已保存: {os.path.basename(file_path)}")
                else:
                    # 显示保存失败消息
                    if hasattr(self.parent_window, 'show_save_error'):
                        self.parent_window.show_save_error("无法保存图片")
                    else:
                        QMessageBox.warning(self, "保存失败", "无法保存图片")
                    
        except Exception as e:
            # 显示保存错误消息
            if hasattr(self.parent_window, 'show_save_error'):
                self.parent_window.show_save_error(f"保存错误：{str(e)}")
            else:
                QMessageBox.warning(self, "保存错误", f"保存错误：{str(e)}")


class ProgressIndicator(QProgressBar):
    """进度指示器组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(6)
        self.setRange(0, 0)  # 设置为不确定模式，显示忙碌状态
        self.setVisible(False)
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 3px;
                background-color: #f1f5f9;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:0.5 #60a5fa, stop:1 #93c5fd);
                border-radius: 3px;
            }
        """)


class ImageDisplayArea(QScrollArea):
    """图片显示区域组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.image_thumbnails = []  # 存储缩略图组件
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # 图片容器
        self.images_container = QWidget()
        self.images_container.setStyleSheet("QWidget { background: transparent; }")
        self.images_layout = QGridLayout(self.images_container)
        self.images_layout.setSpacing(15)
        self.images_layout.setContentsMargins(10, 10, 10, 10)
        
        self.setWidget(self.images_container)
    
    def add_image(self, image_data: str, index: int):
        """添加图片到显示区域"""
        try:
            # 创建缩略图组件
            thumbnail = ImageThumbnail(image_data, index, self.parent_window)
            
            # 计算网格位置
            row = index // 3  # 每行显示3张图片
            col = index % 3
            
            # 添加到布局
            self.images_layout.addWidget(thumbnail, row, col)
            self.image_thumbnails.append(thumbnail)
            
        except Exception as e:
            if hasattr(self.parent_window, 'show_error'):
                self.parent_window.show_error(f"无法显示第 {index+1} 张图片: {str(e)}")
            else:
                QMessageBox.warning(self, "显示错误", f"无法显示第 {index+1} 张图片: {str(e)}")
    
    def clear_images(self):
        """清除所有图片"""
        # 移除所有缩略图组件
        for thumbnail in self.image_thumbnails:
            thumbnail.deleteLater()
        
        self.image_thumbnails.clear()
    
    def get_image_count(self) -> int:
        """获取图片数量"""
        return len(self.image_thumbnails) 