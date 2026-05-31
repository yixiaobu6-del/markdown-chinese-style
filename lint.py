#!/usr/bin/env python3
"""Markdown中文排版规范检查脚本 v2.0 - 增强版"""

import re
import sys
from pathlib import Path


class ChineseLint:
    """中文排版检查器"""

    RULES = {
        "chinese_english_space": {
            "name": "中英文空格",
            "pattern": r'[\u4e00-\u9fff][a-zA-Z0-9]|[a-zA-Z0-9][\u4e00-\u9fff]',
            "message": "中英文/数字之间未加空格",
            "fixable": True,
        },
        "fullwidth_punctuation": {
            "name": "全角标点",
            "pattern": r'[\u4e00-\u9fff][,\.\?!;:][\u4e00-\u9fff]',
            "message": "中文文本使用半角标点，应为全角",
            "fixable": True,
        },
        "line_length": {
            "name": "行长度",
            "message": "超过最大字符数限制",
            "fixable": False,
        },
        "consecutive_blank": {
            "name": "连续空行",
            "pattern": r'\n{4,}',
            "message": "存在连续3个以上空行，建议精简",
            "fixable": True,
        },
        "trailing_space": {
            "name": "行尾空格",
            "pattern": r'[ \t]+$',
            "message": "行尾存在多余空格",
            "fixable": True,
        },
        "mixed_chinese_english": {
            "name": "中英文混排",
            "pattern": r'[\u4e00-\u9fff][\uff01-\uff5e]?[a-zA-Z]{2,}[\u4e00-\u9fff]',
            "message": "中英文混排建议用空格分隔",
            "fixable": False,
        },
        "wrong_quote": {
            "name": "引号检查",
            "pattern": r'[\u4e00-\u9fff]"[^"]*"[\u4e00-\u9fff]',
            "message": "中文内容应使用「」或""代替直引号",
            "fixable": False,
        },
        "heading_spacing": {
            "name": "标题间距",
            "pattern": r'^#+[^ ]',
            "message": "标题标记(#)后应加空格",
            "fixable": True,
        },
    }

    def __init__(self, max_line_length=80):
        self.max_line_length = max_line_length
        self.issues = []
        self.total_checks = 0

    def check_file(self, file_path: str) -> int:
        content = Path(file_path).read_text(encoding='utf-8')
        lines = content.split('\n')
        self.issues = []
        self.total_checks = 0

        # Check per-line rules
        for i, line in enumerate(lines, 1):
            ln = i

            # 中英文空格
            self.total_checks += 1
            if re.search(self.RULES["chinese_english_space"]["pattern"], line):
                self.issues.append((ln, self.RULES["chinese_english_space"]["message"]))

            # 全角标点
            self.total_checks += 1
            if re.search(self.RULES["fullwidth_punctuation"]["pattern"], line):
                self.issues.append((ln, self.RULES["fullwidth_punctuation"]["message"]))

            # 行长度
            self.total_checks += 1
            if len(line) > self.max_line_length and not line.startswith('#'):
                self.issues.append((ln, self.RULES["line_length"]["message"] + f" ({len(line)}>{self.max_line_length})"))

            # 行尾空格
            self.total_checks += 1
            if re.search(self.RULES["trailing_space"]["pattern"], line):
                self.issues.append((ln, self.RULES["trailing_space"]["message"]))

            # 标题间距
            self.total_checks += 1
            if re.search(self.RULES["heading_spacing"]["pattern"], line):
                self.issues.append((ln, self.RULES["heading_spacing"]["message"]))

        # Check multi-line rules
        # 连续空行
        self.total_checks += 1
        if re.search(self.RULES["consecutive_blank"]["pattern"], content):
            self.issues.append((0, self.RULES["consecutive_blank"]["message"]))

        # 中英文混排
        self.total_checks += 1
        if re.search(self.RULES["mixed_chinese_english"]["pattern"], content):
            self.issues.append((0, self.RULES["mixed_chinese_english"]["message"]))

        # 引号检查
        self.total_checks += 1
        wrong_quotes = re.findall(self.RULES["wrong_quote"]["pattern"], content)
        if wrong_quotes:
            self.issues.append((0, f"引号问题：发现 {len(wrong_quotes)} 处"))

        return len(self.issues)

    def report(self, file_path: str) -> bool:
        count = self.check_file(file_path)
        passed = self.total_checks - count

        print(f"\n{'='*50}")
        print(f"检查文件：{file_path}")
        print(f"{'='*50}")
        print(f"总检查项：{self.total_checks}")
        print(f"✅ 通过：{passed} 项")
        print(f"⚠️  问题：{count} 项")
        print(f"通过率：{passed/self.total_checks*100:.0f}%")

        if self.issues:
            print(f"\n问题明细：")
            sorted_issues = sorted(self.issues, key=lambda x: x[0])
            for ln, msg in sorted_issues:
                loc = f"第{ln}行" if ln > 0 else "全文"
                print(f"  [{loc}] {msg}")

        print()
        return count == 0


def lint(file_path: str, max_length: int = 80) -> bool:
    checker = ChineseLint(max_line_length=max_length)
    return checker.report(file_path)


def lint_dir(directory: str, max_length: int = 80) -> None:
    path = Path(directory)
    md_files = list(path.rglob("*.md"))
    total = len(md_files)
    passed = 0

    print(f"批量检查目录：{directory}")
    print(f"找到 {total} 个 Markdown 文件\n")

    for md in md_files:
        if lint(str(md), max_length):
            passed += 1

    print(f"{'='*50}")
    print(f"批量检查完成：{passed}/{total} 通过 ({passed/total*100:.0f}%)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Markdown中文排版检查工具")
    parser.add_argument("path", nargs="?", default=".", help="文件或目录路径")
    parser.add_argument("--max-length", type=int, default=80, help="最大行长度")
    parser.add_argument("--batch", action="store_true", help="批量检查目录")
    args = parser.parse_args()

    path = Path(args.path)

    if args.batch or path.is_dir():
        lint_dir(str(path), args.max_length)
    else:
        lint(str(path), args.max_length)
