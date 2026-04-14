#!/usr/bin/env python3
"""
Markdown to PDF Converter
将 Markdown 文件转换为 PDF，支持中文、表格、代码块等复杂格式

兼容：
- Claude Code (作为技能使用)
- OpenClaw (作为 Skill 使用)
- 命令行工具
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, List

try:
    import markdown
    from weasyprint import HTML
except ImportError:
    print("错误: 缺少依赖库，请运行: pip install markdown weasyprint")
    sys.exit(1)


# 默认 CSS 样式
DEFAULT_CSS = '''
<style>
body {
    font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    margin: 40px;
    color: #333;
}

h1 {
    color: #1a1a1a;
    border-bottom: 2px solid #333;
    padding-bottom: 10px;
    page-break-before: always;
    font-size: 18pt;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    color: #2c3e50;
    margin-top: 30px;
    font-size: 14pt;
    border-bottom: 1px solid #eee;
    padding-bottom: 5px;
}

h3 {
    color: #34495e;
    font-size: 12pt;
}

h4 {
    color: #4a5568;
    font-size: 11pt;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0;
    font-size: 9pt;
}

th, td {
    border: 1px solid #ddd;
    padding: 6px 8px;
    text-align: left;
}

th {
    background-color: #f5f5f5;
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #fafafa;
}

code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
    font-size: 9pt;
}

pre {
    background-color: #f8f8f8;
    padding: 12px;
    border-radius: 5px;
    overflow-x: auto;
    font-size: 8pt;
    line-height: 1.4;
    white-space: pre-wrap;
    word-wrap: break-word;
    border: 1px solid #e0e0e0;
}

pre code {
    background-color: transparent;
    padding: 0;
}

blockquote {
    border-left: 4px solid #3498db;
    margin: 15px 0;
    padding-left: 15px;
    color: #666;
    background-color: #f9f9f9;
    padding: 10px 15px;
    border-radius: 0 5px 5px 0;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 30px 0;
}

ul, ol {
    padding-left: 20px;
}

li {
    margin: 5px 0;
}

img {
    max-width: 100%;
    height: auto;
}

a {
    color: #3498db;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* 页面设置 */
@page {
    size: A4;
    margin: 2cm;
}

/* 打印优化 */
@media print {
    h1, h2, h3 {
        page-break-after: avoid;
    }
    table, pre, blockquote {
        page-break-inside: avoid;
    }
}
</style>
'''


def get_css(custom_css: Optional[str] = None) -> str:
    """获取 CSS 样式，支持自定义"""
    if custom_css and Path(custom_css).exists():
        with open(custom_css, 'r', encoding='utf-8') as f:
            return f'<style>{f.read()}</style>'
    return DEFAULT_CSS


def convert_md_to_pdf(
    input_file: str,
    output_file: Optional[str] = None,
    custom_css: Optional[str] = None,
    title: Optional[str] = None
) -> str:
    """
    将 Markdown 文件转换为 PDF

    Args:
        input_file: 输入的 Markdown 文件路径
        output_file: 输出的 PDF 文件路径（可选，默认同目录）
        custom_css: 自定义 CSS 文件路径（可选）
        title: 文档标题（可选，默认使用文件名）

    Returns:
        生成的 PDF 文件路径
    """
    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_file}")

    if output_file is None:
        output_path = input_path.with_suffix('.pdf')
    else:
        output_path = Path(output_file)

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 读取 Markdown 文件
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 转换为 HTML
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'tables',           # 表格支持
            'fenced_code',      # 代码块支持
            'toc',              # 目录支持
            'nl2br',            # 换行转 <br>
            'sane_lists',       # 更好的列表处理
        ]
    )

    # 获取 CSS 样式
    css = get_css(custom_css)

    # 文档标题
    doc_title = title or input_path.stem

    # 完整的 HTML
    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{doc_title}</title>
    {css}
</head>
<body>
    {html_content}
</body>
</html>
'''

    # 转换为 PDF
    HTML(string=full_html).write_pdf(output_path)

    return str(output_path)


def batch_convert(
    input_dir: str,
    output_dir: Optional[str] = None,
    pattern: str = "*.md",
    custom_css: Optional[str] = None
) -> List[str]:
    """
    批量转换目录下的 Markdown 文件

    Args:
        input_dir: 输入目录
        output_dir: 输出目录（可选，默认为输入目录下的 pdf 子目录）
        pattern: 文件匹配模式（默认 *.md）
        custom_css: 自定义 CSS 文件路径

    Returns:
        生成的 PDF 文件路径列表
    """
    input_path = Path(input_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"目录不存在: {input_dir}")

    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = input_path / 'pdf'

    output_path.mkdir(parents=True, exist_ok=True)

    # 查找所有 Markdown 文件
    md_files = list(input_path.glob(pattern))

    if not md_files:
        print(f"警告: 未找到匹配 '{pattern}' 的文件")
        return []

    print(f"找到 {len(md_files)} 个 Markdown 文件")

    results = []
    for md_file in md_files:
        try:
            pdf_file = output_path / md_file.with_suffix('.pdf').name
            convert_md_to_pdf(str(md_file), str(pdf_file), custom_css)
            print(f"✓ {md_file.name} → {pdf_file.name}")
            results.append(str(pdf_file))
        except Exception as e:
            print(f"✗ {md_file.name}: {e}")

    return results


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='Markdown to PDF 转换工具 - 支持中文、表格、代码块',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s report.md                    # 转换单个文件
  %(prog)s report.md -o output.pdf      # 指定输出文件
  %(prog)s --dir ./docs                 # 批量转换目录
  %(prog)s file1.md file2.md file3.md   # 转换多个文件
  %(prog)s report.md --css custom.css   # 使用自定义样式
        '''
    )

    parser.add_argument('files', nargs='*', help='要转换的 Markdown 文件')
    parser.add_argument('-o', '--output', help='输出文件或目录')
    parser.add_argument('--dir', help='批量转换目录')
    parser.add_argument('--pattern', default='*.md', help='文件匹配模式（默认 *.md）')
    parser.add_argument('--css', help='自定义 CSS 文件')
    parser.add_argument('--title', help='文档标题')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    # 批量转换模式
    if args.dir:
        output_dir = args.output if args.output else None
        results = batch_convert(args.dir, output_dir, args.pattern, args.css)
        print(f"\n完成: 生成 {len(results)} 个 PDF 文件")
        return

    # 单文件或多文件转换模式
    if not args.files:
        parser.print_help()
        return

    for i, file in enumerate(args.files):
        try:
            if args.output and len(args.files) == 1:
                output = args.output
            elif args.output:
                output = str(Path(args.output) / Path(file).with_suffix('.pdf').name)
            else:
                output = None

            result = convert_md_to_pdf(file, output, args.css, args.title)
            size = Path(result).stat().st_size / 1024
            print(f"✓ {Path(file).name} → {Path(result).name} ({size:.1f} KB)")
        except Exception as e:
            print(f"✗ {file}: {e}")


if __name__ == "__main__":
    main()
