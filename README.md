# 🎨 AI 图像生成器

一个基于 PyQt5 和 OpenAI DALL-E API 的本地图像生成器应用程序。用户可以通过输入文本描述来生成高质量的 AI 图像。

## ✨ 功能特性

- 🖊️ **文本到图像生成**: 通过输入描述文本生成相应的图像
- 🔢 **批量生成**: 可同时生成多张图片（1-5张）
- ⚡ **并发处理**: 智能多线程并发调用 API，提高生成效率
- 🖼️ **全屏预览**: 点击图片即可全屏预览，支持缩放和快捷键操作
- 💾 **智能保存**: 自动生成随机文件名，记住保存目录，避免重复
- ⚙️ **配置管理**: 本地持久化保存 API Key 和个性化设置
- 🎨 **现代界面**: 简约现代的设计风格，渐变色彩，圆角阴影
- 📊 **实时进度**: 精美的进度条显示生成状态
- ⏱️ **超时控制**: 可配置超时时间，适应不同生成需求

## 🚀 快速开始

### 环境要求

- Python 3.7+
- OpenAI API Key

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <your-repository-url>
   cd imagica
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置 API Key**
   
   方法一：设置环境变量（推荐）
   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```
   
   方法二：在程序界面中直接输入API Key

4. **运行应用**
   ```bash
   python main.py
   ```

## 📁 项目结构

```
imagica/
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包列表
├── README.md              # 项目说明文档
├── ui/                    # 用户界面模块
│   ├── __init__.py
│   ├── main_window.py     # 主窗口界面
│   ├── image_preview.py   # 图片预览窗口
│   └── fullscreen_preview.py # 全屏预览窗口
├── utils/                 # 工具模块
│   ├── __init__.py
│   ├── image_utils.py     # 图像处理工具
│   └── config_manager.py  # 配置管理
└── assets/               # 资源文件
    └── icon.ico          # 程序图标
```

## 🎯 使用方法

### 基本操作

1. **启动应用**: 运行 `python main.py`
2. **配置API**: 在界面中输入您的API Key和API URL
3. **输入描述**: 在文本框中输入您想要生成的图片描述
4. **设置数量**: 选择要生成的图片数量（1-5张）
5. **开始生成**: 点击"🚀 开始生成"按钮
6. **查看结果**: 等待生成完成，图片将以缩略图形式显示

### 图片操作

- **全屏预览**: 双击缩略图立即进入全屏预览模式
- **窗口预览**: 右键点击图片选择"窗口预览"
- **智能保存**: 右键点击图片选择"保存图片"，自动生成唯一文件名
- **缩放控制**: 全屏模式下使用缩放按钮、键盘快捷键或鼠标滚轮

### 键盘快捷键（全屏预览）

- `Esc`: 退出全屏预览
- `+` 或 `=`: 放大图片
- `-`: 缩小图片
- `0`: 重置缩放到适应屏幕
- `Ctrl+S`: 快速保存图片
- `鼠标滚轮`: 缩放图片
- `右键`: 快速退出

## ⚙️ 配置选项

### API 参数

在程序界面中可以配置：

- **API Key**: 您的OpenAI API密钥
- **API URL**: API服务地址（默认：https://api.apicore.ai/v1/images/generations）

### 生成参数

程序使用以下默认参数（在 `utils/image_utils.py` 中可修改）：

- **model**: "sora_image"
- **size**: "1024x1536" (2:3比例)
- **quality**: "high"
- **style**: "natural"

## 🔧 技术架构

### 核心组件

- **主窗口 (MainWindow)**: 应用程序的主界面，包含所有用户交互控件
- **图像生成线程 (ImageGenerationThread)**: 后台处理图像生成任务，避免界面冻结
- **缩略图组件 (ImageThumbnail)**: 自定义的图片显示组件，支持点击和右键菜单
- **预览窗口 (ImagePreviewWindow)**: 模态对话框，提供图片的放大预览和操作功能
- **全屏预览 (FullScreenPreview)**: 沉浸式全屏图片查看体验
- **图像工具类 (ImageUtils)**: 封装所有图像相关的处理逻辑
- **配置管理器 (ConfigManager)**: 处理应用程序配置的持久化存储

### 技术特点

- **多线程处理**: 使用 `QThread` 和 `ThreadPoolExecutor` 实现并发图像生成
- **信号槽机制**: 利用 PyQt5 的信号槽实现组件间通信
- **Base64 处理**: 使用 Base64 格式处理图像数据，便于网络传输和存储
- **错误处理**: 完善的异常处理机制，确保程序稳定运行

## 📦 打包部署

### 开发环境打包

1. **安装打包工具**
   ```bash
   pip install pyinstaller
   ```

2. **使用批处理脚本打包**
   ```bash
   # Windows用户
   双击运行 打包exe.bat
   ```

3. **手动打包命令**
   ```bash
   pyinstaller --onefile --windowed --name="AI图像生成器" --add-data="assets;assets" --hidden-import=PyQt5.sip --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtWidgets --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=openai --hidden-import=requests --clean --noconfirm main.py
   ```

### 分发说明

生成的exe文件位于 `dist/` 目录下，包含以下特点：
- 单文件exe，约50-100MB
- 包含所有依赖和Python运行时
- 需要确保目标机器有网络连接
- 复制时需要包含 `assets/` 文件夹

## 🐛 故障排除

### 常见问题

1. **API Key 无效**
   - 确保 API Key 正确且有效
   - 检查 API URL 是否正确

2. **网络连接问题**
   - 检查网络连接
   - 确认可以访问配置的 API 地址

3. **依赖包安装失败**
   - 使用 `pip install --upgrade pip` 更新 pip
   - 尝试使用 `pip install -r requirements.txt --force-reinstall`

4. **图片显示异常**
   - 检查 PIL/Pillow 是否正确安装
   - 确认 PyQt5 版本兼容性

### 超时问题解决

如果遇到 "API 请求超时" 错误：

**原因分析**：
- AI 图像生成通常需要 2-5 分钟时间
- 网络延迟会增加总耗时
- 复杂场景描述需要更长时间

**解决方案**：
1. **耐心等待**：程序已设为5分钟超时，请耐心等待
2. **优化提示词**：使用清晰、具体的描述，避免过于复杂的场景
3. **检查网络**：确保网络连接稳定

**超时时间建议**：
- 标准描述：通常 2-3 分钟完成
- 复杂场景：可能需要 3-5 分钟
- 如持续超时，可能是 API 服务问题

### 调试模式

在 `utils/image_utils.py` 中启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔐 安全注意事项

- 不要将API Key提交到版本控制系统
- 定期检查API Key的安全性
- 建议使用环境变量管理敏感配置

## 📄 许可证

本项目采用 MIT 许可证，详情请查看 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

### 贡献指南

1. Fork 本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📞 支持

如果您遇到任何问题或有建议，请：

1. 查看本文档的故障排除章节
2. 提交 [Issue](issues)
3. 联系开发者

## 🎉 致谢

- 感谢 OpenAI 提供强大的图像生成 API
- 感谢 PyQt5 提供优秀的 GUI 框架
- 感谢所有贡献者的支持

---

**享受您的 AI 图像生成之旅！** 🚀✨ 