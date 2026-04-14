# 示例 Markdown 文档

> 这是一个示例文档，用于测试 Markdown 转 PDF 功能

---

## 一、基本格式测试

### 1.1 文本格式

这是**粗体**文本，这是*斜体*文本，这是`代码`文本。

### 1.2 列表测试

无序列表：
- 项目一
- 项目二
- 项目三

有序列表：
1. 第一步
2. 第二步
3. 第三步

### 1.3 引用测试

> 这是一段引用文本
> 可以有多行

---

## 二、表格测试

| 功能 | 支持情况 | 说明 |
|-----|---------|------|
| 中文 | ✅ | 完美支持 |
| 表格 | ✅ | 支持对齐 |
| 代码块 | ✅ | 自动高亮 |
| 图片 | ✅ | 自动缩放 |

---

## 三、代码块测试

### 3.1 Python 代码

```python
def hello_world():
    """Hello World 函数"""
    print("你好，世界！")
    return True

if __name__ == "__main__":
    hello_world()
```

### 3.2 JavaScript 代码

```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
}

greet("World");
```

### 3.3 Shell 命令

```bash
# 安装依赖
pip install markdown weasyprint

# 运行转换
python md2pdf.py example.md
```

---

## 四、数学公式测试

如果支持 LaTeX，可以渲染数学公式：

行内公式：$E = mc^2$

块级公式：

$$
\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n
$$

---

## 五、链接测试

- [GitHub](https://github.com)
- [Python 官网](https://python.org)
- [Markdown 语法](https://markdown.com.cn/)

---

## 六、分割线测试

上面是一条分割线

---

下面是另一条分割线

---

## 七、嵌套结构测试

### 7.1 嵌套列表

1. 第一层
   - 子项目 A
   - 子项目 B
     - 孙项目 X
     - 孙项目 Y
2. 第二层
   - 子项目 C

### 7.2 表格中的代码

| 命令 | 说明 |
|-----|------|
| `pip install` | 安装包 |
| `pip uninstall` | 卸载包 |
| `pip list` | 列出已安装包 |

---

> **文档结束**
> 
> 这是一个完整的 Markdown 测试文档，涵盖了常用的格式元素。
