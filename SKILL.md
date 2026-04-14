---
name: markdown-to-pdf
description: 将 Markdown 文件转换为 PDF，支持中文、表格、代码块等复杂格式
version: 1.0.0
author: Claudian
created: 2026-04-14
tags:
  - pdf
  - markdown
  - conversion
  - document
  - chinese
dependencies:
  - python3 >= 3.8
  - markdown >= 3.4
  - weasyprint >= 60
---

# Markdown 转 PDF 技能

将 Markdown 文件转换为格式美观的 PDF 文档，支持中文、表格、代码块等复杂格式。

## 兼容性

| 平台 | 支持方式 | 说明 |
|-----|---------|------|
| **Claude Code** | 技能文件 | 放置在 `.claude/skills/` 目录 |
| **OpenClaw** | Skill 文件 | 放置在 OpenClaw 的 skills 目录 |
| **命令行** | Python 脚本 | 直接运行 `python md2pdf.py` |

## 快速使用

### Claude Code 中使用

```
用户: 帮我把 report.md 转成 PDF

Claude: [调用 markdown-to-pdf 技能]
✓ report.md → report.pdf (123.4 KB)
```

### OpenClaw 中使用

```
用户: 使用 markdown-to-pdf 技能把 docs 目录下的文件都转成 PDF

OpenClaw: [执行批量转换]
找到 5 个 Markdown 文件
✓ file1.md → file1.pdf
✓ file2.md → file2.pdf
...
完成: 生成 5 个 PDF 文件
```

### 命令行使用

```bash
# 转换单个文件
python md2pdf.py report.md

# 指定输出文件
python md2pdf.py report.md -o output.pdf

# 批量转换目录
python md2pdf.py --dir ./docs

# 使用自定义样式
python md2pdf.py report.md --css custom.css
```

## 功能特性

| 特性 | 说明 |
|-----|------|
| **中文支持** | 自动使用系统中文字体 |
| **表格渲染** | 支持完整的 Markdown 表格语法 |
| **代码高亮** | 代码块自动添加背景和等宽字体 |
| **分页控制** | H1 标题自动分页（除第一个） |
| **目录生成** | 支持 TOC 扩展生成目录 |
| **批量转换** | 支持目录批量处理 |
| **自定义样式** | 支持自定义 CSS 文件 |

## 安装

### 方式一：pip 安装依赖

```bash
pip install markdown weasyprint
```

### 方式二：使用 requirements.txt

```bash
pip install -r requirements.txt
```

## 技能文件格式

### Claude Code 格式

将 `SKILL.md` 放置在 `.claude/skills/` 目录：

```
.claude/
└── skills/
    └── markdown-to-pdf.md
```

### OpenClaw 格式

将技能文件放置在 OpenClaw 的 skills 目录：

```
~/.openclaw/skills/
└── markdown-to-pdf/
    ├── skill.md
    └── md2pdf.py
```

## API 接口

### convert_md_to_pdf()

```python
from md2pdf import convert_md_to_pdf

# 基本用法
pdf_path = convert_md_to_pdf("report.md")

# 指定输出路径
pdf_path = convert_md_to_pdf("report.md", output_file="output/report.pdf")

# 使用自定义样式
pdf_path = convert_md_to_pdf("report.md", custom_css="styles.css")

# 指定标题
pdf_path = convert_md_to_pdf("report.md", title="我的报告")
```

### batch_convert()

```python
from md2pdf import batch_convert

# 批量转换目录
results = batch_convert("./docs")

# 指定输出目录
results = batch_convert("./docs", output_dir="./pdf")

# 使用自定义文件模式
results = batch_convert("./docs", pattern="*.markdown")

# 使用自定义样式
results = batch_convert("./docs", custom_css="styles.css")
```

## 自定义样式

创建自定义 CSS 文件：

```css
/* custom.css */
body {
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 12pt;
}

h1 {
    color: #0066cc;
    border-bottom: 3px solid #0066cc;
}

@page {
    size: A4;
    margin: 2cm;
    @top-center {
        content: "机密文档";
        font-size: 9pt;
        color: #999;
    }
}
```

使用：

```bash
python md2pdf.py report.md --css custom.css
```

## 注意事项

1. **字体要求**：系统需安装中文字体
   - macOS: PingFang SC（系统自带）
   - Windows: Microsoft YaHei（系统自带）
   - Linux: 安装 `fonts-noto-cjk`

2. **性能**：大文件（>1MB）转换可能需要较长时间

3. **内存**：weasyprint 处理复杂文档时内存占用较高

## 故障排除

| 问题 | 解决方案 |
|-----|---------|
| 中文显示为方块 | 安装中文字体 |
| 表格样式错乱 | 检查 Markdown 表格语法 |
| 代码块无样式 | 确保 fenced_code 扩展已启用 |
| PDF 空白 | 检查 HTML 是否正确生成 |

## 许可证

MIT License
