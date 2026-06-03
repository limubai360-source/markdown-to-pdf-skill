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
import html
import re
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
    font-size: 11.5pt;
    line-height: 1.7;
    margin: 0;
    color: #222;
    string-set: doc-title attr(data-doc-title);
}

p {
    margin: 0 0 0.45em 0;
    text-indent: 2em;
    text-align: left;
}

h1 {
    color: #111;
    font-size: 20pt;
    font-weight: 700;
    line-height: 1.35;
    text-align: center;
    margin: 0 0 1.2em 0;
    padding-bottom: 0.55em;
    border-bottom: 2px solid #222;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    color: #1f2d3d;
    font-size: 15pt;
    font-weight: 700;
    line-height: 1.35;
    margin: 1.45em 0 0.65em 0;
    padding: 0 0 0.28em 0.55em;
    border-left: 4px solid #2f5f9f;
    border-bottom: 1px solid #e4e8ee;
    text-indent: 0;
    page-break-after: avoid;
}

h3 {
    color: #263849;
    font-size: 12.5pt;
    font-weight: 700;
    line-height: 1.4;
    margin: 1.05em 0 0.35em 0;
    text-indent: 0;
    page-break-after: avoid;
}

h4 {
    color: #374151;
    font-size: 11.5pt;
    font-weight: 700;
    margin: 0.9em 0 0.3em 0;
    text-indent: 0;
}

strong {
    font-weight: 700;
    color: #111;
}

ul, ol {
    margin: 0.35em 0 0.65em 1.65em;
    padding-left: 0.35em;
    list-style-position: outside;
}

li {
    margin: 0.25em 0;
    padding-left: 0.1em;
}

li p {
    text-indent: 0;
    margin: 0.1em 0 0.25em 0;
}

blockquote {
    margin: 0.75em 0 1em 0;
    padding: 0.65em 0.9em;
    color: #4b5563;
    background: #f7f8fa;
    border-left: 4px solid #9aa8b6;
}

blockquote p {
    text-indent: 0;
    margin: 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.9em 0 1em 0;
    font-size: 9.5pt;
    line-height: 1.45;
}

th, td {
    border: 1px solid #d9dee7;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
}

th {
    background: #f2f4f7;
    font-weight: 700;
}

tr:nth-child(even) {
    background: #fafbfc;
}

code {
    background: #f4f5f7;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
    font-size: 9.5pt;
}

pre {
    background: #f7f8fa;
    padding: 10px 12px;
    border-radius: 5px;
    border: 1px solid #e1e5eb;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.45;
    white-space: pre-wrap;
    word-wrap: break-word;
}

pre code {
    background: transparent;
    padding: 0;
}

hr {
    border: none;
    border-top: 1px solid #e4e8ee;
    margin: 1.4em 0;
}

a {
    color: #1f5f99;
    text-decoration: none;
}

img {
    max-width: 100%;
    height: auto;
}

@page {
    size: A4;
    margin: 2.45cm 2.05cm 2.2cm 2.05cm;
    @top-left {
        content: string(doc-title);
        font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
        font-size: 8.5pt;
        color: #777;
        border-bottom: 1px solid #e6e6e6;
        padding-bottom: 6px;
        width: 100%;
    }
    @bottom-center {
        content: counter(page) " / " counter(pages);
        font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
        font-size: 9pt;
        color: #666;
    }
}

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
    """获取 CSS 样式，支持自定义覆盖。"""
    if custom_css and Path(custom_css).exists():
        with open(custom_css, 'r', encoding='utf-8') as f:
            custom = f.read()
        return f'{DEFAULT_CSS}\n<style>\n{custom}\n</style>'
    return DEFAULT_CSS


_ORDERED_ITEM_RE = re.compile(r'^(\s*)\d+\.\s+')
_HEADING_RE = re.compile(r'^\s*#{1,6}\s+')
_FENCE_RE = re.compile(r'^\s*(```|~~~)')


def normalize_loose_ordered_lists(md_content: str) -> str:
    """Keep loose ordered-list paragraphs inside the same list.

    Python-Markdown treats a numbered heading followed by an unindented
    paragraph as a complete one-item list. Business documents often write
    numbered sections as `1.` + blank line + paragraph, so indent those
    continuation paragraphs before conversion to preserve 1, 2, 3 numbering.
    """
    normalized = []
    in_ordered_list = False
    list_indent = ''

    for line in md_content.splitlines():
        ordered_match = _ORDERED_ITEM_RE.match(line)
        if ordered_match:
            in_ordered_list = True
            list_indent = ordered_match.group(1)
            normalized.append(line)
            continue

        if in_ordered_list:
            stripped = line.strip()
            if not stripped:
                normalized.append(line)
                continue

            if _HEADING_RE.match(line) or _FENCE_RE.match(line):
                in_ordered_list = False
                normalized.append(line)
                continue

            current_indent = len(line) - len(line.lstrip(' '))
            if current_indent <= len(list_indent):
                normalized.append(f'{list_indent}    {line.lstrip()}')
                continue

        normalized.append(line)

    return '\n'.join(normalized)


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
    md_content = normalize_loose_ordered_lists(md_content)
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'tables',           # 表格支持
            'fenced_code',      # 代码块支持
            'toc',              # 目录支持
            'nl2br',            # 换行转 <br>
        ]
    )

    # 获取 CSS 样式
    css = get_css(custom_css)

    # 文档标题
    doc_title = title or input_path.stem
    escaped_title = html.escape(doc_title, quote=True)

    # 完整的 HTML
    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escaped_title}</title>
    {css}
</head>
<body data-doc-title="{escaped_title}">
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
