# Markdown 中文排版规范

> 统一中文Markdown排版标准，含lint检查脚本

---

## Features / 功能特点

| 功能 | 说明 |
|------|------|
| 中英文混排空格 | 中文与英文/数字之间必须加空格 |
| 全角标点规则 | 中文文本使用全角标点（，。！？；：） |
| 专有名词规范 | 英文专有名词保持原样大小写 |
| 段落格式规范 | 段落空行、段首无空格、单行80字符 |
| 标题层级规范 | 一级至四级标题使用规范 |
| 列表格式规范 | 无序/有序列表格式规范 |
| 链接格式规范 | 链接语法标准格式 |
| 强调格式规范 | 粗体、斜体、代码格式规范 |
| 代码块规范 | 语言标注、代码块格式规范 |
| 自动检查脚本 | lint.py 自动检查 Markdown 文件 |

## Installation / 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/markdown-chinese-style-guide.git

cd markdown-chinese-style-guide
```

## Usage / 使用方法

### 基础用法：使用 lint.py 检查

```bash
# 检查单个文件
python lint.py your_file.md

# 输出示例：
# ✅ 通过：5项
# ❌ 问题：2项
#   - 第3行：中英文未加空格
#   - 第5行：使用半角标点

# 检查多个文件
python lint.py *.md

# 输出详细报告
python lint.py your_file.md --verbose
```

### 核心规则速查

#### 1. 中英文混排空格

```
正确：使用 Claude Code 编写代码
错误：使用Claude Code编写代码

正确：版本 2.0 发布
错误：版本2.0发布
```

#### 2. 全角标点

```
正确：这是一个例子，说明了规则。
错误：这是一个例子,说明了规则.
```

#### 3. 专有名词

```
正确：GitHub、Claude Code、Python
错误：github、claude code、python
```

### VS Code 配置

安装插件：`markdownlint`

配置 `.markdownlint.json`：

```json
{
  "MD001": true,
  "MD003": {"style": "atx"},
  "MD009": {"br_spaces": 2},
  "MD013": {"line_length": 80}
}
```

## Contributing / 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)

欢迎贡献：
- 补充排版规则
- 改进 lint.py 脚本
- 提供规则示例

## License / 许可证

MIT License - 参见 [LICENSE](LICENSE)

---

> 版本：1.0.0 | 更新日期：2026-05-30