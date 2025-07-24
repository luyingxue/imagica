# -*- coding: utf-8 -*-
"""
UI组件模块
包含可重用的用户界面组件
"""

from PyQt5.QtWidgets import (
    QLabel, QPushButton, QFrame, QHBoxLayout, QVBoxLayout,
    QSlider, QPlainTextEdit, QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class ModernButton(QPushButton):
    """现代化按钮组件"""
    
    def __init__(self, text: str, color: str = "#3b82f6", primary: bool = True, parent=None):
        super().__init__(text, parent)
        self.color = color
        self.primary = primary
        self.setup_style()
    
    def setup_style(self):
        """设置按钮样式"""
        if self.primary:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {self.color}, stop:1 {self.darken_color(self.color, 10)});
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
                        stop:0 {self.lighten_color(self.color, 10)}, stop:1 {self.color});
                }}
                QPushButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {self.darken_color(self.color, 20)}, stop:1 {self.darken_color(self.color, 10)});
                }}
                QPushButton:disabled {{
                    background: #94a3b8;
                    color: #f1f5f9;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(255, 255, 255, 0.8);
                    color: {self.color};
                    border: 2px solid {self.color};
                    border-radius: 12px;
                    padding: 6px 12px;
                    font-size: 11px;
                    font-weight: bold;
                    font-family: "Microsoft YaHei UI";
                    min-width: 70px;
                }}
                QPushButton:hover {{
                    background: {self.color};
                    color: white;
                }}
                QPushButton:pressed {{
                    background: {self.darken_color(self.color, 10)};
                    border-color: {self.darken_color(self.color, 10)};
                }}
            """)
    
    def lighten_color(self, color: str, percent: int) -> str:
        """浅化颜色"""
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


class HeaderComponent(QFrame):
    """头部组件"""
    
    def __init__(self, title: str = "AI 图像生成器", subtitle: str = "AI Image Generator", parent=None):
        super().__init__(parent)
        self.title = title
        self.subtitle = subtitle
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffffff, stop:1 #f1f5f9);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 12px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # Logo 图标
        logo_label = QLabel("🎨")
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                color: #3b82f6;
            }
        """)
        layout.addWidget(logo_label)
        
        # 标题文字
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setFamily("Microsoft YaHei UI")
        title_label.setFont(font)
        title_label.setStyleSheet("""
            QLabel {
                color: #1e293b;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # 副标题
        subtitle_label = QLabel(self.subtitle)
        subtitle_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Segoe UI")
        subtitle_label.setFont(font)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #64748b;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(subtitle_label)


class SectionFrame(QFrame):
    """章节框架组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 12px;
            }
        """)


class SectionTitle(QLabel):
    """章节标题组件"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setFamily("Microsoft YaHei UI")
        self.setFont(font)
        self.setStyleSheet("""
            QLabel {
                color: #334155;
                margin-bottom: 5px;
            }
        """)


class CustomTextEdit(QPlainTextEdit):
    """自定义文本编辑器"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(80)
        self.setMaximumHeight(150)
        
        # 设置换行模式
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.setStyleSheet("""
            QPlainTextEdit {
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 12px;
                font-size: 12px;
                font-family: "Microsoft YaHei UI";
                background: #fefefe;
                selection-background-color: #3b82f6;
                selection-color: white;
                line-height: 1.4;
            }
            QPlainTextEdit:focus {
                border-color: #3b82f6;
            }
        """)


class CustomLineEdit(QLineEdit):
    """自定义行编辑器"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
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


class NumberSlider(QFrame):
    """数字滑动器组件"""
    
    value_changed = pyqtSignal(int)
    
    def __init__(self, title: str = "数量", min_val: int = 1, max_val: int = 5, default_val: int = 3, parent=None):
        super().__init__(parent)
        self.title = title
        self.min_val = min_val
        self.max_val = max_val
        self.default_val = default_val
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        self.setStyleSheet("QFrame { background: transparent; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        # 标题行
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题
        title_label = QLabel(f"🔢 {self.title}")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setFamily("Microsoft YaHei UI")
        title_label.setFont(font)
        title_label.setStyleSheet("""
            QLabel {
                color: #334155;
                padding: 0px;
            }
        """)
        title_layout.addWidget(title_label)
        
        # 数量显示标签
        self.display_label = QLabel(str(self.default_val))
        self.display_label.setFont(font)
        self.display_label.setStyleSheet("""
            QLabel {
                color: #3b82f6;
                background-color: #eff6ff;
                border: 2px solid #3b82f6;
                border-radius: 12px;
                padding: 6px 12px;
                min-width: 20px;
                min-height: 14px;
                text-align: center;
            }
        """)
        self.display_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.display_label)
        
        layout.addLayout(title_layout)
        
        # 滑动条
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(self.min_val, self.max_val)
        self.slider.setValue(self.default_val)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #e2e8f0;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f1f5f9, stop:1 #e2e8f0);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3b82f6, stop:1 #1d4ed8);
                border: 2px solid #ffffff;
                width: 20px;
                height: 20px;
                margin: -8px 0;
                border-radius: 12px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2563eb, stop:1 #1e40af);
                border: 2px solid #ffffff;
            }
            QSlider::handle:horizontal:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1d4ed8, stop:1 #1e3a8a);
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #60a5fa);
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: #e2e8f0;
                border-radius: 4px;
            }
        """)
        
        # 连接信号
        self.slider.valueChanged.connect(self.update_display)
        self.slider.valueChanged.connect(self.value_changed.emit)
        
        layout.addWidget(self.slider)
        
        # 刻度标签
        tick_layout = QHBoxLayout()
        tick_layout.setContentsMargins(0, 0, 0, 0)
        for i in range(self.min_val, self.max_val + 1):
            tick_label = QLabel(str(i))
            tick_label.setStyleSheet("""
                QLabel {
                    color: #64748b;
                    font-size: 10px;
                    text-align: center;
                }
            """)
            tick_label.setAlignment(Qt.AlignCenter)
            if i == self.min_val:
                tick_layout.addWidget(tick_label)
            else:
                tick_layout.addStretch()
                tick_layout.addWidget(tick_label)
        
        layout.addLayout(tick_layout)
    
    def update_display(self, value: int):
        """更新显示数值"""
        self.display_label.setText(str(value))
    
    def value(self) -> int:
        """获取当前值"""
        return self.slider.value()
    
    def setValue(self, value: int):
        """设置值"""
        self.slider.setValue(value)


class OptionSelector(QFrame):
    """通用选项选择器组件"""
    
    option_changed = pyqtSignal(str)
    
    def __init__(self, title: str, options: dict, default_key: str = None, parent=None):
        super().__init__(parent)
        self.title = title
        self.options = options  # {key: display_name}
        self.default_key = default_key or list(options.keys())[0]
        self.current_key = self.default_key
        self.buttons = []
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        self.setStyleSheet("QFrame { background: transparent; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        # 标题
        title_label = QLabel(self.title)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setFamily("Microsoft YaHei UI")
        title_label.setFont(font)
        title_label.setStyleSheet("""
            QLabel {
                color: #334155;
                padding: 0px;
            }
        """)
        layout.addWidget(title_label)
        
        # 选项按钮
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(4)
        
        for key, display_name in self.options.items():
            btn = QPushButton(display_name)
            btn.setCheckable(True)
            btn.setChecked(key == self.default_key)
            btn.clicked.connect(lambda checked, k=key: self.select_option(k))
            
            # 设置按钮样式 - 简化版本，无复杂效果
            btn.setStyleSheet("""
                QPushButton {
                    background: #f8fafc;
                    color: #64748b;
                    border: 2px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-size: 11px;
                    font-weight: bold;
                    font-family: "Microsoft YaHei UI";
                    min-width: 50px;
                    min-height: 26px;
                }
                QPushButton:hover {
                    background: #e2e8f0;
                    border-color: #cbd5e1;
                }
                QPushButton:checked {
                    background: #3b82f6;
                    color: white;
                    border-color: #2563eb;
                }
                QPushButton:checked:hover {
                    background: #2563eb;
                }
            """)
            
            self.buttons.append(btn)
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
    
    def select_option(self, key: str):
        """选择选项"""
        self.current_key = key
        
        # 更新按钮状态
        for btn in self.buttons:
            btn.setChecked(False)
        
        # 设置选中按钮
        for i, (k, _) in enumerate(self.options.items()):
            if k == key:
                self.buttons[i].setChecked(True)
                break
        
        # 发出信号
        self.option_changed.emit(key)
    
    def get_current_key(self) -> str:
        """获取当前选择的key"""
        return self.current_key
    
    def get_current_value(self) -> str:
        """获取当前选择的显示名称"""
        return self.options[self.current_key]


class RatioSelector(OptionSelector):
    """比例选择器"""
    
    def __init__(self, parent=None):
        options = {
            "1024x1536": "竖屏",
            "1536x1024": "横屏"
        }
        super().__init__("📐 比例", options, "1024x1536", parent)


class ModelSelector(OptionSelector):
    """模型选择器"""
    
    def __init__(self, parent=None):
        options = {
            "sora_image": "Sora",
            "gpt-image-1": "GPT-4o"
        }
        super().__init__("🤖 模型", options, "sora_image", parent)


 