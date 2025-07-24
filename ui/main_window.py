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
from PyQt5.QtGui import QIcon, QFont

from utils.config_manager import config_manager
from ui.components import (
    HeaderComponent, SectionFrame, SectionTitle, 
    CustomTextEdit, CustomLineEdit, ModernButton, NumberSlider,
    RatioSelector, ModelSelector
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

    def create_api_section(self):
        """创建API设置区域"""
        section = SectionFrame()
        layout = QVBoxLayout(section)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # API设置标题
        title = SectionTitle("🔑 API 设置")
        layout.addWidget(title)
        
        # API Key 输入
        api_key_layout = QHBoxLayout()
        
        api_key_label = QLabel("API Key:")
        api_key_label.setAlignment(Qt.AlignCenter)
        api_key_label.setStyleSheet("color: #334155; min-width: 80px;")
        api_key_layout.addWidget(api_key_label)
        
        self.api_key_edit = CustomLineEdit("请输入您的 API Key")
        self.api_key_edit.setEchoMode(self.api_key_edit.Password)
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
        
        self.api_url_edit = CustomLineEdit("https://api.apicore.ai/v1/images/generations")
        api_url_layout.addWidget(self.api_url_edit)
        
        # 保存按钮
        self.save_api_btn = ModernButton("💾 保存设置", primary=False)
        self.save_api_btn.clicked.connect(self.save_api_settings)
        api_url_layout.addWidget(self.save_api_btn)
        
        layout.addLayout(api_url_layout)
        
        # 加载已保存的设置
        self.load_api_settings()
        
        return section

    def create_control_section(self):
        """创建控制区域"""
        section = SectionFrame()
        layout = QHBoxLayout(section)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignVCenter)  # 设置垂直居中对齐
        
        # 数量滑动器
        self.number_slider = NumberSlider("生成数量", 1, 5, 3)
        layout.addWidget(self.number_slider, 0, Qt.AlignVCenter)
        
        # 添加分隔线（视觉分隔）
        separator = QLabel("|")
        separator.setStyleSheet("color: #e2e8f0; font-size: 18px; margin: 0 8px;")
        separator.setAlignment(Qt.AlignCenter)
        layout.addWidget(separator, 0, Qt.AlignVCenter)
        
        # 比例选择器
        self.ratio_selector = RatioSelector()
        layout.addWidget(self.ratio_selector, 0, Qt.AlignVCenter)
        
        # 添加分隔线
        separator2 = QLabel("|")
        separator2.setStyleSheet("color: #e2e8f0; font-size: 18px; margin: 0 8px;")
        separator2.setAlignment(Qt.AlignCenter)
        layout.addWidget(separator2, 0, Qt.AlignVCenter)
        
        # 模型选择器
        self.model_selector = ModelSelector()
        layout.addWidget(self.model_selector, 0, Qt.AlignVCenter)
        
        layout.addStretch()
        
        # 使用优化的生成按钮 - 更大尺寸但无动画
        self.generate_btn = ModernButton("🚀 开始生成", "#3b82f6", True)
        self.generate_btn.setMinimumHeight(60)  # 设置更大的高度
        self.generate_btn.setMinimumWidth(130)
        # 重写样式使其更醒目
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3b82f6, stop:0.5 #60a5fa, stop:1 #2563eb);
                color: white;
                border: 3px solid #2563eb;
                border-radius: 15px;
                padding: 15px 25px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Microsoft YaHei UI";
                min-width: 120px;
                min-height: 50px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2563eb, stop:0.5 #3b82f6, stop:1 #1d4ed8);
                border: 4px solid #1d4ed8;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1d4ed8, stop:0.5 #2563eb, stop:1 #1e3a8a);
                border: 3px solid #1e3a8a;
            }
            QPushButton:disabled {
                background: #94a3b8;
                color: #f1f5f9;
                border: 3px solid #64748b;
            }
        """)
        layout.addWidget(self.generate_btn, 0, Qt.AlignVCenter)
        
        return section

    def create_progress_section(self):
        """创建进度区域"""
        section = SectionFrame()
        layout = QVBoxLayout(section)
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
        
        # 使用自定义进度指示器
        self.progress_bar = ProgressIndicator()
        layout.addWidget(self.progress_bar)
        
        return section

    def create_images_section(self):
        """创建图片显示区域"""
        section = SectionFrame()
        layout = QVBoxLayout(section)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = SectionTitle("🖼️ 生成的图片")
        layout.addWidget(title)
        
        # 创建图片显示区域
        self.image_display = ImageDisplayArea(self)
        layout.addWidget(self.image_display)
        
        return section



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
        
        num_images = self.number_slider.value()
        
        # 获取选择的比例和模型
        selected_size = self.ratio_selector.get_current_key()
        selected_model = self.model_selector.get_current_key()
        
        # 清除之前的图片
        self.image_display.clear_images()
        
        # 更新界面状态
        self.generate_btn.setEnabled(False)
        self.progress_label.setText(f"🔄 正在生成 {num_images} 张图片...\n⏳ 每张图片可能需要 2-3 分钟，请耐心等待")
        self.progress_bar.setVisible(True)
        
        # 启动生成线程
        self.generation_thread = ImageGenerationThread(prompt, num_images, api_key, selected_size, selected_model)
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
            # 使用图片显示区域添加图片
            self.image_display.add_image(image_data, index)
            self.generated_images.append(image_data)
            
        except Exception as e:
            QMessageBox.warning(self, "显示错误", f"无法显示第 {index+1} 张图片: {str(e)}")

    def generation_finished(self):
        """图片生成完成"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setText(f"✅ 完成！共生成 {self.image_display.get_image_count()} 张图片")

    def show_error(self, error_message: str):
        """显示错误信息"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setText("❌ 生成失败")
        QMessageBox.warning(self, "生成错误", error_message)

    def show_save_success(self, message: str):
        """显示保存成功消息"""
        self.progress_label.setText(f"💾 {message}")
        # 3秒后恢复原状态
        QTimer.singleShot(3000, lambda: self.progress_label.setText("📊 准备就绪"))

    def show_save_error(self, message: str):
        """显示保存错误消息"""
        self.progress_label.setText(f"❌ {message}")
        # 3秒后恢复原状态
        QTimer.singleShot(3000, lambda: self.progress_label.setText("📊 准备就绪"))
    

 