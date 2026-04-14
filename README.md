# Markdown to PDF Skill

<div align="center">

**将 Markdown 文件转换为 PDF，支持中文、表格、代码块等复杂格式**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green.svg)](https://claude.ai)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-green.svg)](https://github.com/OpenClaw/openclaw)

</div>

---

## ✨ 特性

- 🇨🇳 **完美中文支持** - 自动使用系统中文字体
- 📊 **表格渲染** - 支持完整的 Markdown 表格语法
- 💻 **代码高亮** - 代码块自动添加背景和等宽字体
- 📄 **分页控制** - H1 标题自动分页
- 📑 **目录生成** - 支持 TOC 扩展
- 🔄 **批量转换** - 支持目录批量处理
- 🎨 **自定义样式** - 支持自定义 CSS
- 🔧 **多平台兼容** - Claude Code、OpenClaw、命令行

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/limubai360-source/markdown-to-pdf-skill.git

# 安装依赖
pip install markdown weasyprint
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

## 🚀 快速开始

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

### Python API

```python
from md2pdf import convert_md_to_pdf, batch_convert

# 转换单个文件
pdf_path = convert_md_to_pdf("report.md")

# 批量转换
results = batch_convert("./docs", output_dir="./pdf")
```

## 🔌 平台集成

### Claude Code

将 `SKILL.md` 复制到 Claude Code 的技能目录：

```bash
mkdir -p ~/.claude/skills
cp SKILL.md ~/.claude/skills/markdown-to-pdf.md
```

使用方式：

```
用户: 帮我把 report.md 转成 PDF

Claude: [调用 markdown-to-pdf 技能]
✓ report.md → report.pdf (123.4 KB)
```

### OpenClaw

将项目复制到 OpenClaw 的 skills 目录：

```bash
mkdir -p ~/.openclaw/skills/markdown-to-pdf
cp -r ./* ~/.openclaw/skills/markdown-to-pdf/
```

使用方式：

```
用户: 使用 markdown-to-pdf 技能把 docs 目录转成 PDF

OpenClaw: [执行批量转换]
找到 5 个 Markdown 文件
✓ file1.md → file1.pdf
...
```

## 📖 文档

### 命令行参数

| 参数 | 说明 |
|-----|------|
| `files` | 要转换的 Markdown 文件（支持多个） |
| `-o, --output` | 输出文件或目录 |
| `--dir` | 批量转换目录 |
| `--pattern` | 文件匹配模式（默认 `*.md`） |
| `--css` | 自定义 CSS 文件 |
| `--title` | 文档标题 |

### API 接口

#### convert_md_to_pdf()

```python
convert_md_to_pdf(
    input_file: str,           # 输入文件路径
    output_file: str = None,   # 输出文件路径（可选）
    custom_css: str = None,    # 自定义 CSS 文件（可选）
    title: str = None          # 文档标题（可选）
) -> str                       # 返回 PDF 文件路径
```

#### batch_convert()

```python
batch_convert(
    input_dir: str,            # 输入目录
    output_dir: str = None,    # 输出目录（可选）
    pattern: str = "*.md",     # 文件匹配模式
    custom_css: str = None     # 自定义 CSS 文件
) -> List[str]                 # 返回 PDF 文件路径列表
```

## 🎨 自定义样式

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
    }
}
```

使用：

```bash
python md2pdf.py report.md --css custom.css
```

## 📁 项目结构

```
markdown-to-pdf-skill/
├── md2pdf.py           # 核心转换脚本
├── SKILL.md            # 技能定义文件（Claude Code / OpenClaw）
├── README.md           # 项目说明
├── requirements.txt    # Python 依赖
├── setup.py            # 安装脚本
├── LICENSE             # 许可证
├── examples/           # 示例文件
│   ├── sample.md       # 示例 Markdown
│   └── custom.css      # 示例样式
└── tests/              # 测试文件
    └── test_md2pdf.py
```

## ⚠️ 注意事项

### 字体要求

| 系统 | 推荐字体 | 安装方式 |
|-----|---------|---------|
| macOS | PingFang SC | 系统自带 |
| Windows | Microsoft YaHei | 系统自带 |
| Linux | Noto Sans CJK | `apt install fonts-noto-cjk` |

### 性能说明

- 小文件（<100KB）：转换时间 <1s
- 中等文件（100KB-1MB）：转换时间 1-5s
- 大文件（>1MB）：转换时间可能较长

## 🔧 故障排除

| 问题 | 解决方案 |
|-----|---------|
| 中文显示为方块 | 安装中文字体 |
| 表格样式错乱 | 检查 Markdown 表格语法 |
| 代码块无样式 | 确保 fenced_code 扩展已启用 |
| PDF 空白 | 检查 HTML 是否正确生成 |
| 内存不足 | 尝试分批转换大文件 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [markdown](https://python-markdown.github.io/) - Python Markdown 解析库
- [weasyprint](https://weasyprint.org/) - HTML 到 PDF 转换引擎
- [Claude Code](https://claude.ai/) - AI 编程助手
- [OpenClaw](https://github.com/OpenClaw/openclaw) - 开源 AI Agent

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

</div>
