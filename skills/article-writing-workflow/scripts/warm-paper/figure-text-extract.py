#!/usr/bin/env python3
"""配图 HTML 里的可见文字提取成 Markdown，供 yomiyasu_lint 检查日文图内文字。

用法: python3 figure-text-extract.py <图目录> [-o 输出.md]
每张图一个 `## <文件名>` 小节，每个文字元素一段。跳过 _ 开头的备份目录与文件。
"""
import argparse
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SKIP_TAGS = {"style", "script", "head", "title", "defs"}


class TextCollector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.parts = []
        self.buf = ""

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip_depth += 1
        self.flush()

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        self.flush()

    def handle_data(self, data):
        if not self.skip_depth:
            self.buf += data

    def flush(self):
        text = re.sub(r"\s+", " ", self.buf).strip()
        if text:
            self.parts.append(html.unescape(text))
        self.buf = ""


def extract(path: Path) -> list[str]:
    parser = TextCollector()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.flush()
    return parser.parts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("folder", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    if not args.folder.is_dir():
        print(f"目录不存在: {args.folder}", file=sys.stderr)
        return 1
    files = sorted(p for p in args.folder.glob("*.html") if not p.name.startswith("_"))
    if not files:
        print(f"没有配图 HTML: {args.folder}", file=sys.stderr)
        return 1
    out = []
    for f in files:
        out.append(f"## {f.stem}\n")
        out.extend(f"{t}\n" for t in extract(f))
    md = "\n".join(out)
    if args.output:
        args.output.write_text(md, encoding="utf-8")
        print(f"{len(files)} 张图 → {args.output}")
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
