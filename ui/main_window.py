# -*- coding: utf-8 -*-
"""
主窗口界面
使用模块化组件构建的主窗口
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

from utils.config_manager import config_manager
from ui.components import (
    HeaderComponent, SectionFrame, SectionTitle, 
    CustomTextEdit, CustomLineEdit, ModernButton, NumberSlider
)
from ui.widgets import (
    ImageGenerationThread, ProgressIndicator, ImageDisplayArea
)


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.generated_images = []  # 存储生成的图片数据
        self.generation_thread = None
        
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("AI 图像生成器")
        self.setMinimumSize(900, 700)
        self.resize(1200, 800)
        
        # 设置应用程序图标
        self.setWindowIcon(QIcon("assets/icon.ico"))
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8fafc, stop:1 #e2e8f0);
            }
        """)
        
        # 设置中央组件
        central_widget = QWidget()
        central_widget.setStyleSheet("QWidget { background: transparent; }")
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建各个区域
        self.header = HeaderComponent()
        self.api_section = self.create_api_section()
        self.input_section = self.create_input_section()
        self.control_section = self.create_control_section()
        self.progress_section = self.create_progress_section()
        self.images_section = self.create_images_section()
        
        # 添加到主布局
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.api_section)
        main_layout.addWidget(self.input_section)
        main_layout.addWidget(self.control_section)
        main_layout.addWidget(self.progress_section)
        main_layout.addWidget(self.images_section, 1)  # 图片区域占据剩余空间

    def create_input_section(self):
        """创建输入区域"""
        section = SectionFrame()
        layout = QVBoxLayout(section)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 添加标题
        title = SectionTitle("📝 描述您想要生成的图片")
        layout.addWidget(title)
        
        # 添加文本输入框
        self.prompt_edit = CustomTextEdit(
            placeholder="请输入图片描述，例如：一只可爱的小猫在花园里玩耍，阳光明媚，高分辨率..."
        )
        layout.addWidget(self.prompt_edit)
        
        return section

    def create_control_section(self):
        """创建控制区域"""
        section = SectionFrame()
        layout = QHBoxLayout(section)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 数量滑动器
        self.number_slider = NumberSlider("生成数量", 1, 5, 3)
        layout.addWidget(self.number_slider)
        
        layout.addStretch()
        
        # 生成按钮
        self.generate_btn = ModernButton("🚀 开始生成")
        layout.addWidget(self.generate_btn)
        
        return section
    
    def create_api_area(self):
        """创建API设置区域"""
        self.api_group = QFrame()
        self.api_group.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self.api_group)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # API设置标题
        api_title = QLabel("🔑 API 设置")
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setFamily("Microsoft YaHei UI")
        api_title.setFont(font)
        api_title.setStyleSheet("""
            QLabel {
                color: #334155;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(api_title)
        
        # API Key 输入
        api_key_layout = QHBoxLayout()
        
        api_key_label = QLabel("API Key:")
        api_key_label.setAlignment(Qt.AlignCenter)
        api_key_label.setStyleSheet("color: #334155; min-width: 80px;")
        api_key_layout.addWidget(api_key_label)
        
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        self.api_key_edit.setPlaceholderText("请输入您的 API Key")
        self.api_key_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 11px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        api_key_layout.addWidget(self.api_key_edit)
        
        # 显示/隐藏密码按钮
        self.toggle_password_btn = QPushButton("👁")
        self.toggle_password_btn.setFixedSize(28, 28)
        self.toggle_password_btn.setStyleSheet("""
            QPushButton {
                background: #f1f5f9;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #e2e8f0;
            }
        """)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        api_key_layout.addWidget(self.toggle_password_btn)
        
        layout.addLayout(api_key_layout)
        
        # API URL 输入
        api_url_layout = QHBoxLayout()
        
        api_url_label = QLabel("API URL:")
        api_url_label.setAlignment(Qt.AlignCenter)
        api_url_label.setStyleSheet("color: #334155; min-width: 80px;")
        api_url_layout.addWidget(api_url_label)
        
        self.api_url_edit = QLineEdit()
        self.api_url_edit.setPlaceholderText("https://api.apicore.ai/v1/images/generations")
        self.api_url_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 11px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        api_url_layout.addWidget(self.api_url_edit)
        
        # 保存按钮
        self.save_api_btn = QPushButton("💾 保存设置")
        self.save_api_btn.setStyleSheet("""
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """)
        self.save_api_btn.clicked.connect(self.save_api_settings)
        api_url_layout.addWidget(self.save_api_btn)
        
        layout.addLayout(api_url_layout)
        
        # 加载已保存的设置
        self.load_api_settings()
    
    def toggle_password_visibility(self):
        """切换密码可见性"""
        if self.api_key_edit.echoMode() == QLineEdit.Password:
            self.api_key_edit.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("🙈")
        else:
            self.api_key_edit.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("👁")
    
    def load_api_settings(self):
        """加载API设置"""
        api_key = config_manager.get_api_key()
        api_url = config_manager.get_api_url()
        
        if api_key:
            self.api_key_edit.setText(api_key)
        if api_url:
            self.api_url_edit.setText(api_url)
    
    def save_api_settings(self):
        """保存API设置"""
        api_key = self.api_key_edit.text().strip()
        api_url = self.api_url_edit.text().strip()
        
        if not api_key:
            QMessageBox.warning(self, "输入错误", "请输入 API Key")
            return
        
        if not api_url:
            QMessageBox.warning(self, "输入错误", "请输入 API URL")
            return
        
        # 保存设置
        config_manager.set_api_key(api_key)
        config_manager.set_api_url(api_url)
        
        QMessageBox.information(self, "保存成功", "API 设置已保存")
    
    def create_modern_button(self, text: str, color: str, primary: bool = False) -> QPushButton:
        """创建现代化按钮"""
        btn = QPushButton(text)
        
        if primary:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {color}, stop:1 {self.darken_color(color, 10)});
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 6px 12px;
                    font-size: 11px;
                    font-weight: bold;
                    font-family: "Microsoft YaHei UI";
                    min-width: 90px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {self.lighten_color(color, 10)}, stop:1 {color});
                }}
                QPushButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {self.darken_color(color, 20)}, stop:1 {self.darken_color(color, 10)});
                }}
                QPushButton:disabled {{
                    background: #94a3b8;
                    color: #f1f5f9;
                }}
            """)
        else:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(255, 255, 255, 0.8);
                    color: {color};
                    border: 2px solid {color};
                    border-radius: 12px;
                    padding: 6px 12px;
                    font-size: 11px;
                    font-weight: bold;
                    font-family: "Microsoft YaHei UI";
                    min-width: 70px;
                }}
                QPushButton:hover {{
                    background: {color};
                    color: white;
                }}
                QPushButton:pressed {{
                    background: {self.darken_color(color, 10)};
                    border-color: {self.darken_color(color, 10)};
                }}
            """)
        
        return btn
    
    def lighten_color(self, color: str, percent: int) -> str:
        """浅化颜色"""
        # 简单实现，实际可以使用更复杂的颜色计算
        color_map = {
            "#3b82f6": "#60a5fa",
            "#ef4444": "#f87171",
            "#64748b": "#94a3b8"
        }
        return color_map.get(color, color)
    
    def darken_color(self, color: str, percent: int) -> str:
        """深化颜色"""
        color_map = {
            "#3b82f6": "#2563eb",
            "#ef4444": "#dc2626",
            "#64748b": "#475569"
        }
        return color_map.get(color, color)

    def create_progress_area(self):
        """创建进度区域"""
        self.progress_group = QFrame()
        self.progress_group.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self.progress_group)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 12, 15, 12)
        
        self.progress_label = QLabel("📊 准备就绪")
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Microsoft YaHei UI")
        self.progress_label.setFont(font)
        self.progress_label.setStyleSheet("""
            QLabel {
                color: #334155;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(self.progress_label)
        
        # 使用 QProgressBar 创建发光运动效果
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setRange(0, 0)  # 设置为不确定模式，显示忙碌状态
        self.progress_bar.setStyleSheet("""
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
                animation: glow 2s ease-in-out infinite alternate;
            }
        """)
        layout.addWidget(self.progress_bar)

    def create_images_area(self):
        """创建图片显示区域"""
        self.images_group = QFrame()
        self.images_group.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self.images_group)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        images_label = QLabel("🖼️ 生成的图片")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setFamily("Microsoft YaHei UI")
        images_label.setFont(font)
        images_label.setStyleSheet("""
            QLabel {
                color: #334155;
                margin-bottom: 8px;
            }
        """)
        layout.addWidget(images_label)
        
        # 滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
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
        
        self.scroll_area.setWidget(self.images_container)
        layout.addWidget(self.scroll_area)

    def setup_connections(self):
        """设置信号连接"""
        self.generate_btn.clicked.connect(self.start_generation)

    def start_generation(self):
        """开始生成图片"""
        prompt = self.prompt_edit.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "输入错误", "请输入图片描述")
            return
        
        # 检查 API Key
        api_key = self.api_key_edit.text().strip()
        if not api_key:
            QMessageBox.warning(self, "输入错误", "请输入 API Key")
            return
        
        num_images = self.num_images_slider.value()
        
        # 清除之前的图片
        self.clear_images()
        
        # 更新界面状态
        self.generate_btn.setEnabled(False)
        self.progress_label.setText(f"🔄 正在生成 {num_images} 张图片...\n⏳ 每张图片可能需要 2-3 分钟，请耐心等待")
        self.progress_bar.setVisible(True)
        
        # 启动生成线程
        self.generation_thread = ImageGenerationThread(prompt, num_images, api_key)
        self.generation_thread.progress_updated.connect(self.update_progress)
        self.generation_thread.image_generated.connect(self.add_generated_image)
        self.generation_thread.generation_completed.connect(self.generation_finished)
        self.generation_thread.error_occurred.connect(self.show_error)
        self.generation_thread.start()

    def update_progress(self, value: int):
        """更新进度条（保持发光运动效果）"""
        # 进度条保持不确定模式，显示发光运动效果
        pass

    def add_generated_image(self, index: int, image_data: str):
        """添加生成的图片"""
        try:
            # 创建缩略图组件
            thumbnail = ImageThumbnail(image_data, index, self)
            
            # 计算网格位置
            row = index // 3  # 每行显示3张图片
            col = index % 3
            
            # 添加到布局
            self.images_layout.addWidget(thumbnail, row, col)
            self.image_thumbnails.append(thumbnail)
            self.generated_images.append(image_data)
            
        except Exception as e:
            QMessageBox.warning(self, "显示错误", f"无法显示第 {index+1} 张图片: {str(e)}")

    def generation_finished(self):
        """图片生成完成"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setText(f"✅ 完成！共生成 {len(self.generated_images)} 张图片")

    def show_error(self, error_message: str):
        """显示错误信息"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setText("❌ 生成失败")
        QMessageBox.warning(self, "生成错误", error_message)

    def clear_images(self):
        """清除所有图片"""
        # 移除所有缩略图组件
        for thumbnail in self.image_thumbnails:
            thumbnail.deleteLater()
        
        self.image_thumbnails.clear()
        self.generated_images.clear()
        
        # 重置进度显示
        self.progress_label.setText("📊 准备就绪")
        self.progress_bar.setVisible(False)
    
    # 移除复杂的showEvent和apply_text_wrapping方法，简化换行设置
    # def showEvent(self, event):
    #     """窗口显示事件"""
    #     super().showEvent(event)
    #     # 窗口显示后立即应用换行设置
    #     QTimer.singleShot(100, self.apply_text_wrapping)
    
    # def apply_text_wrapping(self):
    #     """应用文本换行设置"""
    #     try:
    #         from PyQt5.QtGui import QTextOption
    #         text_option = QTextOption()
    #         text_option.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
    #         self.prompt_edit.document().setDefaultTextOption(text_option)
    #         # 强制重新绘制
    #         self.prompt_edit.viewport().update()
    #         # 强制重新计算大小
    #         self.prompt_edit.updateGeometry()
    #     except Exception as e:
    #         print(f"应用换行设置时出错: {e}")
     
    def update_num_display(self):
        """更新生成数量显示标签"""
        self.num_display_label.setText(str(self.num_images_slider.value()))

 