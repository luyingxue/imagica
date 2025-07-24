#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 图像生成器安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# 读取requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

# 读取版本信息
def get_version():
    """从constants.py读取版本号"""
    try:
        from config.constants import APP_VERSION
        return APP_VERSION
    except ImportError:
        return "2.0.0"

setup(
    name="ai-image-generator",
    version=get_version(),
    author="AI Image Generator Team",
    author_email="contact@example.com",
    description="基于 CustomTkinter 和 OpenAI API 的轻量级图像生成器",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/ai-image-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0", 
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "build": [
            "pyinstaller>=5.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-image-generator=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*", "config/*", "*.md", "*.txt"],
    },
    keywords=[
        "ai", "image", "generator", "openai", "dall-e", "customtkinter", 
        "gui", "desktop", "application", "art", "creative"
    ],
    project_urls={
        "Bug Reports": "https://github.com/your-username/ai-image-generator/issues",
        "Source": "https://github.com/your-username/ai-image-generator",
        "Documentation": "https://github.com/your-username/ai-image-generator#readme",
        "Changelog": "https://github.com/your-username/ai-image-generator/blob/main/CHANGELOG.md",
    },
) 