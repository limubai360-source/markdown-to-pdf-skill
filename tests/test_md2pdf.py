#!/usr/bin/env python3
"""
Markdown to PDF Converter - Unit Tests
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from md2pdf import convert_md_to_pdf, batch_convert, get_css


class TestMd2Pdf(unittest.TestCase):
    """md2pdf 模块测试"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.sample_md = """
# 测试文档

这是一个测试文档。

## 表格测试

| 列1 | 列2 |
|-----|-----|
| A   | B   |

## 代码测试

```python
print("Hello")
```
"""

    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_convert_md_to_pdf_basic(self):
        """测试基本转换功能"""
        # 创建测试文件
        md_file = Path(self.temp_dir) / "test.md"
        md_file.write_text(self.sample_md, encoding='utf-8')

        # 转换
        pdf_path = convert_md_to_pdf(str(md_file))

        # 验证
        self.assertTrue(os.path.exists(pdf_path))
        self.assertTrue(pdf_path.endswith('.pdf'))
        self.assertTrue(os.path.getsize(pdf_path) > 0)

    def test_convert_md_to_pdf_with_output(self):
        """测试指定输出路径"""
        md_file = Path(self.temp_dir) / "input.md"
        md_file.write_text(self.sample_md, encoding='utf-8')

        output_file = Path(self.temp_dir) / "output.pdf"

        pdf_path = convert_md_to_pdf(str(md_file), str(output_file))

        self.assertEqual(pdf_path, str(output_file))
        self.assertTrue(output_file.exists())

    def test_convert_md_to_pdf_file_not_found(self):
        """测试文件不存在的情况"""
        with self.assertRaises(FileNotFoundError):
            convert_md_to_pdf("nonexistent.md")

    def test_batch_convert(self):
        """测试批量转换"""
        # 创建多个测试文件
        for i in range(3):
            md_file = Path(self.temp_dir) / f"test{i}.md"
            md_file.write_text(f"# 测试文档 {i}\n\n内容 {i}", encoding='utf-8')

        # 批量转换
        output_dir = Path(self.temp_dir) / "pdf"
        results = batch_convert(self.temp_dir, str(output_dir))

        # 验证
        self.assertEqual(len(results), 3)
        for pdf_path in results:
            self.assertTrue(os.path.exists(pdf_path))

    def test_batch_convert_empty_dir(self):
        """测试空目录"""
        empty_dir = Path(self.temp_dir) / "empty"
        empty_dir.mkdir()

        results = batch_convert(str(empty_dir))

        self.assertEqual(len(results), 0)

    def test_get_css_default(self):
        """测试默认 CSS"""
        css = get_css()

        self.assertIn('<style>', css)
        self.assertIn('font-family', css)
        self.assertIn('PingFang SC', css)

    def test_chinese_content(self):
        """测试中文内容"""
        chinese_md = """
# 中文测试

这是一段中文内容。

## 表格

| 名称 | 描述 |
|-----|------|
| 测试 | 这是一个测试 |
| 示例 | 这是一个示例 |

## 列表

- 第一项
- 第二项
- 第三项
"""
        md_file = Path(self.temp_dir) / "chinese.md"
        md_file.write_text(chinese_md, encoding='utf-8')

        pdf_path = convert_md_to_pdf(str(md_file))

        self.assertTrue(os.path.exists(pdf_path))
        self.assertTrue(os.path.getsize(pdf_path) > 0)

    def test_code_block(self):
        """测试代码块"""
        code_md = """
# 代码测试

```python
def hello():
    print("Hello, World!")
    return True

if __name__ == "__main__":
    hello()
```

```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
}
```
"""
        md_file = Path(self.temp_dir) / "code.md"
        md_file.write_text(code_md, encoding='utf-8')

        pdf_path = convert_md_to_pdf(str(md_file))

        self.assertTrue(os.path.exists(pdf_path))

    def test_table(self):
        """测试表格"""
        table_md = """
# 表格测试

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A   | B   | C   |
| D   | E   | F   |
| G   | H   | I   |
"""
        md_file = Path(self.temp_dir) / "table.md"
        md_file.write_text(table_md, encoding='utf-8')

        pdf_path = convert_md_to_pdf(str(md_file))

        self.assertTrue(os.path.exists(pdf_path))


class TestCLI(unittest.TestCase):
    """命令行接口测试"""

    def test_import_main(self):
        """测试 main 函数可导入"""
        from md2pdf import main
        self.assertTrue(callable(main))


if __name__ == '__main__':
    unittest.main(verbosity=2)
