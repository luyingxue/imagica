# 开发指南

本文档为 AI 图像生成器项目的开发人员提供详细的开发指南。

## 项目架构

### 目录结构

```
imagica/
├── main.py                    # 应用程序入口点
├── requirements.txt           # 生产环境依赖
├── requirements-dev.txt       # 开发环境依赖
├── config/                    # 配置模块
│   ├── __init__.py
│   └── constants.py          # 应用程序常量
├── ui/                       # 用户界面模块
│   ├── __init__.py
│   ├── main_window.py        # 主窗口
│   ├── components.py         # UI组件
│   └── widgets.py           # 自定义控件
├── utils/                    # 工具模块
│   ├── __init__.py
│   ├── config_manager.py     # 配置管理器
│   ├── image_utils.py        # 图像处理工具
│   ├── logger.py            # 日志管理器
│   ├── exceptions.py        # 自定义异常
│   └── validators.py        # 输入验证器
├── tests/                   # 测试模块
│   ├── __init__.py
│   ├── test_config.py
│   └── test_validators.py
├── docs/                    # 项目文档
├── logs/                    # 日志文件目录
├── assets/                  # 静态资源
└── release/                 # 发布文件
```

### 核心模块

#### 1. 配置模块 (config/)
- **constants.py**: 定义所有应用程序常量
- 包含UI配置、API配置、错误消息等
- 提供集中的配置管理

#### 2. 用户界面模块 (ui/)
- **main_window.py**: 主窗口类，应用程序的主要界面
- **components.py**: 可重用的UI组件
- **widgets.py**: 自定义控件和复杂组件

#### 3. 工具模块 (utils/)
- **config_manager.py**: 配置文件的读写管理
- **image_utils.py**: 图像处理和API调用
- **logger.py**: 统一的日志记录系统
- **exceptions.py**: 自定义异常类型
- **validators.py**: 输入数据验证

## 开发环境设置

### 1. 克隆项目
```bash
git clone <repository-url>
cd imagica
```

### 2. 创建虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖
```bash
# 安装开发依赖（包含生产依赖）
pip install -r requirements-dev.txt
```

### 4. 配置开发工具
```bash
# 安装pre-commit钩子
pre-commit install

# 配置代码格式化
black --check .
isort --check-only .
flake8 .
```

## 代码规范

### 1. 代码风格
- 使用 Black 进行代码格式化
- 使用 isort 管理导入语句
- 使用 flake8 进行代码质量检查
- 遵循 PEP 8 编码规范

### 2. 命名规范
- 类名使用 PascalCase：`MainWindow`
- 函数和变量使用 snake_case：`get_api_key`
- 常量使用大写：`API_CONFIG`
- 私有方法使用下划线前缀：`_setup_logging`

### 3. 文档字符串
```python
def example_function(param1: str, param2: int) -> bool:
    """
    函数功能的简短描述
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述
        
    Returns:
        返回值的描述
        
    Raises:
        Exception: 异常情况的描述
    """
    pass
```

### 4. 类型注解
- 所有公共方法都应该包含类型注解
- 使用 typing 模块提供的类型
- 复杂类型使用 Union、Optional 等

## 测试

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_config.py

# 运行测试并生成覆盖率报告
pytest --cov=. --cov-report=html
```

### 测试规范
- 每个模块都应该有对应的测试文件
- 测试类命名：`TestClassName`
- 测试方法命名：`test_method_name`
- 使用 pytest 的 fixture 进行测试设置

## 日志记录

### 使用日志
```python
from utils.logger import get_logger, log_exception, log_user_action

# 获取日志记录器
logger = get_logger(__name__)

# 记录普通信息
logger.info("应用程序启动")

# 记录异常
try:
    # 一些可能出错的代码
    pass
except Exception as e:
    log_exception(logger, e, "操作失败")

# 记录用户操作
log_user_action(logger, "生成图像", "用户生成了3张图像")
```

### 日志级别
- DEBUG: 详细的调试信息
- INFO: 普通的信息消息
- WARNING: 警告消息
- ERROR: 错误消息
- CRITICAL: 严重错误

## 异常处理

### 使用自定义异常
```python
from utils.exceptions import ValidationException, APIException

# 抛出验证异常
if not api_key:
    raise ValidationException("API Key 不能为空", field="api_key")

# 捕获特定异常
try:
    # API 调用
    pass
except APIException as e:
    logger.error(f"API 错误: {e.message}")
    # 处理API错误
except ValidationException as e:
    logger.error(f"验证错误: {e.message}")
    # 处理验证错误
```

## 配置管理

### 使用常量
```python
from config.constants import WINDOW_CONFIG, ERROR_MESSAGES, ICONS

# 使用窗口配置
self.geometry(WINDOW_CONFIG["geometry"])

# 使用错误消息
messagebox.showerror("错误", ERROR_MESSAGES["no_api_key"])

# 使用图标
button.configure(text=f"{ICONS['save']} 保存")
```

### 添加新常量
1. 在 `config/constants.py` 中添加常量
2. 在 `config/__init__.py` 中导出
3. 更新相关文档

## 构建和部署

### 开发环境运行
```bash
python main.py
```

### 打包为exe
```bash
# 使用完整版打包脚本
python build_exe.py

# 使用轻量级打包脚本
python build_exe_simple.py
```

### 版本发布
1. 更新版本号（在 `config/constants.py` 中）
2. 更新 CHANGELOG.md
3. 运行所有测试
4. 构建发布包
5. 创建git标签

## 贡献指南

### 提交代码
1. 创建功能分支：`git checkout -b feature/new-feature`
2. 编写代码和测试
3. 运行代码质量检查：`pre-commit run --all-files`
4. 提交代码：`git commit -m "Add new feature"`
5. 推送分支：`git push origin feature/new-feature`
6. 创建Pull Request

### 代码审查
- 确保所有测试通过
- 检查代码覆盖率
- 验证代码风格符合规范
- 检查文档更新

## 常见问题

### Q: 如何添加新的UI组件？
A: 在 `ui/components.py` 中添加新的组件类，确保继承适当的父类并遵循现有的设计模式。

### Q: 如何添加新的验证规则？
A: 在 `utils/validators.py` 中的相应验证器类中添加新方法，并在 `config/constants.py` 中更新验证配置。

### Q: 如何处理新的异常类型？
A: 在 `utils/exceptions.py` 中定义新的异常类，并在 `ExceptionHandler` 中添加相应的处理方法。

### Q: 如何调试日志问题？
A: 检查 `logs/` 目录中的日志文件，调整 `config/constants.py` 中的 `LOG_CONFIG` 设置。 