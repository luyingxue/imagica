# -*- coding: utf-8 -*-
"""
应用程序常量配置
定义应用程序中使用的所有常量值
"""

# 应用程序基本信息
APP_NAME = "AI 图像生成器"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "基于 CustomTkinter 和 OpenAI API 的轻量级图像生成器"

# 窗口配置
WINDOW_CONFIG = {
    "title": f"{APP_NAME} - CustomTkinter Version",
    "geometry": "1000x800",
    "min_size": (800, 600),
    "appearance_mode": "dark",
    "color_theme": "blue"
}

# UI 尺寸常量
UI_SIZES = {
    "header_height": 80,
    "button_height": 80,
    "button_width": 80,
    "entry_height": 35,
    "textbox_height": 100,
    "thumbnail_width": 180,
    "thumbnail_height": 270,
    "thumbnail_image_width": 160,
    "thumbnail_image_height": 240,
    "corner_radius": 12,
    "small_corner_radius": 8,
    "large_corner_radius": 15
}

# UI 间距常量
UI_SPACING = {
    "large_padding": 15,
    "medium_padding": 10,
    "small_padding": 5,
    "grid_padx": 15,
    "grid_pady": 15
}

# 颜色配置
COLORS = {
    "primary": ("#2563eb", "#1d4ed8"),
    "primary_hover": ("#1d4ed8", "#1e3a8a"),
    "success": ("green", "lightgreen"),
    "error": ("red", "lightcoral"),
    "warning": ("orange", "yellow"),
    "disabled": ("gray70", "gray40"),
    "text_secondary": ("gray60", "gray40"),
    "background": ("gray90", "gray20")
}

# API 配置
API_CONFIG = {
    "default_url": "https://api.apicore.ai/v1/images/generations",
    "timeout": 300,  # 5分钟
    "max_retries": 3,
    "models": {
        "sora_image": "Sora",
        "gpt-image-1": "GPT-4o"
    },
    "sizes": {
        "1024x1536": "竖屏 (2:3)",
        "1536x1024": "横屏 (3:2)"
    },
    "generation_params": {
        "background": "opaque",
        "moderation": "auto",
        "output_format": "png",
        "quality": "high",
        "style": "natural",
        "output_compression": 100,
        "response_format": "b64_json"
    }
}

# 生成参数配置
GENERATION_CONFIG = {
    "min_images": 1,
    "max_images": 5,
    "default_images": 3,
    "default_size": "1024x1536",
    "default_model": "sora_image"
}

# 文件路径配置
PATHS = {
    "config_file": ".apikey",
    "log_dir": "logs",
    "assets_dir": "assets",
    "icon_file": "assets/icon.ico",
    "logo_file": "assets/logo.ico",
    "default_save_dir": "~/Pictures"
}

# 快捷键配置
SHORTCUTS = {
    "exit_fullscreen": ["Escape"],
    "zoom_in": ["plus", "equal"],
    "zoom_out": ["minus"],
    "reset_zoom": ["0"],
    "save_image": ["s", "S"],
    "close_preview": ["Right_Click"]
}

# 错误消息
ERROR_MESSAGES = {
    "no_prompt": "请输入图像描述",
    "no_api_key": "请输入 API Key",
    "invalid_api_key": "API Key 无效或为空",
    "api_request_failed": "API 请求失败",
    "api_timeout": "API 请求超时",
    "network_error": "网络连接错误",
    "image_load_failed": "图像加载失败",
    "image_save_failed": "图像保存失败",
    "config_load_failed": "配置文件加载失败",
    "config_save_failed": "配置文件保存失败",
    "invalid_response": "API 响应格式无效",
    "generation_failed": "图像生成失败"
}

# 成功消息
SUCCESS_MESSAGES = {
    "api_settings_saved": "API 设置已保存",
    "image_saved": "图像已保存",
    "config_loaded": "配置已加载",
    "generation_complete": "图像生成完成",
    "all_generation_complete": "所有图像生成完成"
}

# 状态消息
STATUS_MESSAGES = {
    "ready": "📊 准备就绪",
    "generating": "🔄 正在生成图像...",
    "saving": "💾 正在保存图像...",
    "loading": "⏳ 正在加载...",
    "api_testing": "🔗 正在测试 API 连接...",
    "complete": "✅ 完成！"
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5,
    "encoding": "utf-8"
}

# 字体配置
FONTS = {
    "title": {"size": 20, "weight": "bold"},
    "subtitle": {"size": 14, "weight": "bold"},
    "body": {"size": 12},
    "small": {"size": 11},
    "button": {"size": 13, "weight": "bold"},
    "large_emoji": {"size": 28}
}

# 图标和emoji
ICONS = {
    "app": "🎨",
    "api_key": "🔑",
    "description": "📝",
    "generate": "🚀",
    "save": "💾",
    "preview": "🖼️",
    "fullscreen": "⛶",
    "settings": "⚙️",
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "loading": "⏳",
    "zoom_in": "🔍+",
    "zoom_out": "🔍-",
    "reset": "⚡",
    "exit": "❌",
    "show": "👁",
    "hide": "🙈",
    "aspect_ratio": "📐",
    "model": "🤖",
    "number": "🔢"
}

# 占位符文本
PLACEHOLDERS = {
    "api_key": "输入您的 API Key",
    "api_url": "https://api.apicore.ai/v1/images/generations",
    "prompt": "输入图像描述，例如：一只可爱的小猫在花园里玩耍，阳光明媚，高分辨率..."
}

# 验证规则
VALIDATION = {
    "api_key_min_length": 8,
    "prompt_min_length": 5,
    "prompt_max_length": 2000,
    "url_pattern": r"^https?://.+",
    "supported_image_formats": [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
}

# 性能配置
PERFORMANCE = {
    "thumbnail_cache_size": 50,
    "max_concurrent_generations": 5,
    "image_load_timeout": 30,
    "ui_update_interval": 100  # 毫秒
} 