#!/usr/bin/env python3
"""
Markdown to PDF Converter - Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="md2pdf",
    version="1.0.0",
    author="Claudian",
    author_email="claudian@example.com",
    description="将 Markdown 文件转换为 PDF，支持中文、表格、代码块等复杂格式",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/markdown-to-pdf-skill",
    py_modules=["md2pdf"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Office/Business :: Office Suites",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "markdown>=3.4.0",
        "weasyprint>=60.0",
    ],
    entry_points={
        "console_scripts": [
            "md2pdf=md2pdf:main",
        ],
    },
    keywords="markdown pdf converter chinese claude-code openclaw",
)
