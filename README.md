# 🎨 AI 图像生成器 - 重构优化版

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

一个基于 **CustomTkinter** 和 **OpenAI API** 的现代化轻量级图像生成器应用程序。经过全面重构优化，相比原版本**体积减少75%以上**，性能提升显著，代码质量大幅改善。

## ✨ 主要特性

### 🚀 核心功能
- 🖊️ **智能图像生成**: 基于文本描述生成高质量 AI 图像
- 🔢 **批量处理**: 支持同时生成1-5张图片，智能并发处理
- ⚡ **异步架构**: 多线程并发调用 API，显著提升生成效率
- 🖼️ **多样预览**: 缩略图、窗口预览、全屏预览多种查看方式
- 💾 **智能保存**: 自动生成唯一文件名，记忆保存目录
- ⚙️ **配置管理**: 本地持久化存储，支持多环境配置

### 🎯 技术优势
- 📦 **轻量级**: 打包后仅15-25MB（相比PyQt5版本的100MB+）
- ⚡ **高性能**: 启动速度提升60%+，内存占用减少50%+
- 🎨 **现代界面**: CustomTkinter 暗色主题，符合现代设计趋势
- 🔧 **易维护**: 模块化架构，清晰的代码结构
- 🛡️ **稳定可靠**: 完善的错误处理和日志记录系统
- 🧪 **测试覆盖**: 单元测试保证代码质量

### 🆕 重构优化亮点
- **架构重设计**: 模块化分层架构，职责分离
- **错误处理**: 完善的异常处理和用户友好的错误提示
- **日志系统**: 轮转日志记录，便于问题诊断
- **输入验证**: 严格的数据验证，提高应用稳定性
- **常量管理**: 集中化配置管理，易于维护
- **代码质量**: 类型注解、文档字符串、单元测试

## 🏗️ 项目架构

### 📁 目录结构
```
imagica/
├── 📄 main.py                    # 应用程序入口点
├── 📋 requirements.txt           # 生产环境依赖
├── 📋 requirements-dev.txt       # 开发环境依赖
├── ⚙️ config/                    # 配置模块
│   ├── __init__.py
│   └── constants.py             # 应用程序常量配置
├── 🎨 ui/                       # 用户界面模块
│   ├── __init__.py
│   ├── main_window.py           # 主窗口类
│   ├── components.py            # 可重用UI组件
│   └── widgets.py              # 自定义控件
├── 🛠️ utils/                    # 工具模块
│   ├── __init__.py
│   ├── config_manager.py        # 配置管理器
│   ├── image_utils.py           # 图像处理工具
│   ├── logger.py               # 日志管理器
│   ├── exceptions.py           # 自定义异常
│   └── validators.py           # 输入验证器
├── 🧪 tests/                   # 测试模块
│   ├── __init__.py
│   ├── test_config.py
│   └── test_validators.py
├── 📚 docs/                    # 项目文档
│   └── DEVELOPMENT.md          # 开发指南
├── 📋 logs/                    # 日志文件目录
├── 🖼️ assets/                  # 静态资源文件
└── 📦 release/                 # 发布文件目录
```

### 🔧 核心模块说明

| 模块 | 职责 | 主要功能 |
|------|------|----------|
| **config** | 配置管理 | 应用常量、UI配置、API配置 |
| **ui** | 用户界面 | 主窗口、组件、控件 |
| **utils** | 工具服务 | 配置、日志、验证、异常处理 |
| **tests** | 质量保证 | 单元测试、集成测试 |
| **docs** | 文档说明 | 开发指南、API文档 |

## 🚀 快速开始

### 📋 环境要求

- **Python**: 3.7+ 
- **OpenAI API Key**: 有效的API密钥
- **网络连接**: 用于调用API服务
- **操作系统**: Windows、macOS、Linux

### 🔧 安装步骤

1. **克隆项目**
   ```bash
   git clone <your-repository-url>
   cd imagica
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   # 生产环境
   pip install -r requirements.txt
   
   # 开发环境（包含测试工具）
   pip install -r requirements-dev.txt
   ```

4. **配置 API Key**
   
   **方法一：环境变量（推荐）**
   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```
   
   **方法二：程序界面**
   - 启动应用后在"🔑 API Settings"区域输入

5. **运行应用**
   ```bash
   python main.py
   ```

## 🎯 使用指南

### 🖥️ 基本操作流程

1. **启动应用**: 运行 `python main.py`
2. **配置API**: 在"🔑 API Settings"区域输入API Key和URL
3. **输入描述**: 在"📝 Describe"区域输入图片描述
4. **调整参数**: 
   - 🔢 **生成数量**: 1-5张图片
   - 📐 **图片比例**: 竖屏(2:3) 或 横屏(3:2)
   - 🤖 **AI模型**: Sora 或 GPT-4o
5. **开始生成**: 点击"🚀 生成"按钮
6. **查看结果**: 生成的图片将显示为缩略图

### 🖼️ 图片操作

- **🖱️ 单击缩略图**: 直接进入全屏预览
- **🖱️ 右键菜单**:
  - 🖼️ **窗口预览**: 在弹窗中查看
  - ⛶ **全屏预览**: 沉浸式全屏体验
  - 💾 **保存图片**: 保存到本地

### ⌨️ 快捷键（全屏预览）

| 快捷键 | 功能 |
|--------|------|
| `Esc` | 退出全屏预览 |
| `+` / `=` | 放大图片 |
| `-` | 缩小图片 |
| `0` | 重置缩放 |
| `S` | 快速保存 |
| `右键` | 退出预览 |

## ⚙️ 配置说明

### 🔑 API 配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| **API Key** | OpenAI API密钥 | 需要用户提供 |
| **API URL** | API服务地址 | `https://api.apicore.ai/v1/images/generations` |
| **超时设置** | 请求超时时间 | 300秒（5分钟） |
| **重试次数** | 失败重试次数 | 3次 |

### 🎨 生成参数

| 参数 | 选项 | 说明 |
|------|------|------|
| **模型** | Sora, GPT-4o | AI生成模型 |
| **尺寸** | 1024x1536, 1536x1024 | 图片分辨率 |
| **质量** | high | 生成质量 |
| **风格** | natural | 图片风格 |
| **格式** | PNG | 输出格式 |

## 🔧 开发指南

### 🛠️ 开发环境设置

1. **安装开发依赖**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **配置代码质量工具**
   ```bash
   # 安装pre-commit钩子
   pre-commit install
   
   # 代码格式化
   black .
   isort .
   
   # 代码检查
   flake8 .
   mypy .
   ```

3. **运行测试**
   ```bash
   # 运行所有测试
   pytest
   
   # 生成覆盖率报告
   pytest --cov=. --cov-report=html
   ```

### 📚 架构设计原则

- **单一职责**: 每个模块只负责一个功能领域
- **依赖注入**: 通过接口解耦，便于测试和维护
- **配置外置**: 所有配置集中管理，避免硬编码
- **异常统一**: 自定义异常类型，提供明确的错误信息
- **日志规范**: 结构化日志记录，便于问题诊断

### 🧪 测试策略

- **单元测试**: 覆盖核心业务逻辑
- **集成测试**: 验证模块间协作
- **UI测试**: 确保界面功能正常
- **性能测试**: 监控内存和响应时间

## 📦 打包部署

### 🔨 构建exe文件

**Windows用户（推荐）**:
```bash
# 双击运行批处理文件
打包exe.bat
```

**命令行打包**:
```bash
# 完整功能版本
python build_exe.py

# 轻量级版本
python build_exe_simple.py
```

### 📊 打包优化特性

✅ **智能排除**: 自动排除PyQt、numpy等重型库  
✅ **UPX压缩**: 支持进一步压缩（可选）  
✅ **依赖精简**: 只包含必需的模块  
✅ **启动优化**: 减少冷启动时间  

### 📈 性能对比

| 指标 | PyQt5版本 | CustomTkinter版本 | 改善幅度 |
|------|-----------|-------------------|----------|
| **打包体积** | 80-120MB | 15-25MB | ⬇️ **75%+** |
| **启动时间** | 3-5秒 | 1-2秒 | ⬇️ **60%+** |
| **内存占用** | 150-200MB | 60-100MB | ⬇️ **50%+** |
| **响应速度** | 一般 | 流畅 | ⬆️ **显著提升** |

## 🐛 故障排除

### ❓ 常见问题解决

<details>
<summary><strong>🔑 API Key 相关问题</strong></summary>

**问题**: API Key 无效  
**解决方案**:
- 确保API Key正确且有效
- 检查API URL是否正确
- 验证账户余额是否充足
- 查看日志文件获取详细错误信息

</details>

<details>
<summary><strong>🌐 网络连接问题</strong></summary>

**问题**: 网络请求失败  
**解决方案**:
- 检查网络连接状态
- 确认可以访问配置的API地址
- 检查防火墙和代理设置
- 尝试使用不同的API端点

</details>

<details>
<summary><strong>📦 依赖安装问题</strong></summary>

**问题**: 依赖包安装失败  
**解决方案**:
```bash
# 升级pip
pip install --upgrade pip

# 清理缓存重装
pip cache purge
pip install -r requirements.txt --force-reinstall

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

</details>

<details>
<summary><strong>🖼️ 图片显示异常</strong></summary>

**问题**: 图片无法显示  
**解决方案**:
- 确认PIL/Pillow正确安装
- 检查CustomTkinter版本兼容性
- 查看日志文件中的错误信息
- 重启应用程序

</details>

### 📋 日志诊断

应用程序会在 `logs/` 目录中生成详细的日志文件：

```bash
logs/
├── app_20240724.log    # 当日日志
├── app_20240723.log    # 历史日志
└── ...
```

**日志级别说明**:
- `INFO`: 正常操作记录
- `WARNING`: 警告信息
- `ERROR`: 错误信息  
- `DEBUG`: 详细调试信息

## 📄 开源协议

本项目采用 **MIT 许可证**，详情请查看 [LICENSE](LICENSE) 文件。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

### 🛠️ 贡献流程

1. **Fork** 本项目到你的账户
2. **创建特性分支**: `git checkout -b feature/AmazingFeature`
3. **提交修改**: `git commit -m 'Add some AmazingFeature'`
4. **推送分支**: `git push origin feature/AmazingFeature`
5. **提交 Pull Request**

### 📝 贡献内容

- 🐛 **Bug修复**: 修复已知问题
- ✨ **新功能开发**: 添加有用的新特性
- 📚 **文档改进**: 完善项目文档
- 🎨 **UI/UX优化**: 改善用户体验
- ⚡ **性能提升**: 优化应用性能
- 🧪 **测试增强**: 增加测试覆盖率

### 📋 开发规范

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 编码规范
- 使用 `black` 进行代码格式化
- 添加必要的类型注解和文档字符串
- 编写单元测试覆盖新功能
- 更新相关文档

## 📞 支持与反馈

如果您遇到任何问题或有建议，请：

1. 📖 查看本文档的故障排除章节
2. 🔍 搜索现有的 [Issues](../../issues)
3. 🐛 提交新的 [Issue](../../issues/new) 报告问题
4. 💬 参与 [Discussions](../../discussions) 讨论
5. 📧 联系开发团队

## 🎉 致谢

- 🙏 感谢 **OpenAI** 提供强大的图像生成 API
- 🙏 感谢 **CustomTkinter** 提供现代化的GUI框架
- 🙏 感谢 **PIL/Pillow** 提供图像处理支持
- 🙏 感谢所有贡献者和用户的支持与反馈

## 🌟 更新日志

### v2.0.0 - 架构重构版 (2024-07-24)

#### 🔄 重大变更
- **完全重构**: 从PyQt5迁移到CustomTkinter
- **架构重设计**: 模块化分层架构，职责清晰分离
- **性能优化**: 打包体积减少75%+，启动速度提升60%+

#### ✨ 新增功能
- **日志系统**: 完善的轮转日志记录
- **异常处理**: 自定义异常类型和统一错误处理
- **输入验证**: 严格的数据验证机制
- **配置管理**: 集中化常量和配置管理
- **单元测试**: 核心功能的测试覆盖

#### 🎨 界面改进
- **现代化设计**: 暗色主题，符合现代审美
- **交互优化**: 更流畅的用户体验
- **错误提示**: 用户友好的错误信息

#### 🔧 开发体验
- **代码质量**: 类型注解、文档字符串、代码规范
- **开发工具**: pre-commit、black、flake8、pytest
- **文档完善**: 开发指南、架构说明、贡献指南

#### 🐛 问题修复
- 修复配置管理器调用错误
- 改善API错误处理
- 优化图像加载性能
- 增强应用稳定性

### v1.x.x - PyQt5版本（已停止维护）
- 历史版本，基于PyQt5框架
- 功能完整但体积较大
- 不再提供更新支持

---

**享受您的轻量级 AI 图像生成之旅！** 🚀✨ 