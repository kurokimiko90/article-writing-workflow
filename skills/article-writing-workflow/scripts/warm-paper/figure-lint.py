"""配図の機械チェック。審図 Agent が人の目で探さなくて済む問題を先に拾う。

使い方:
  python3 figure-lint.py <diagrams_dir> [--article article.md] [--source <原文版の diagrams_dir>]

検査（× は exit 1、! は警告のみ）:
  ! 焦点が2つ   見出しの <mark> と図内の莱姆要素が別の語（同じ讯息かは審図で判断）
  × palt       中国語の図で font-feature-settings:"palt"（全角の，：が半角のように詰まる）
  × 中国語残り  日本語版の図に、仮名を含まない中国語の文字列が残っている
  ! 本文にない  図の数字・英単語が本文に出てこない（内部情報・新しい数字の持ち込み）
  ! 構造の差    翻訳版の図が原文版と菱形・カードの数で食い違う（工程の欠落など）
  ! 截圖が広い  本文が参照するスクリーンショットの幅が 2400px を超える（記事幅で UI の字が読めない）
2026-10-26 の4記事の審図で繰り返し出た指摘から作った。
"""
import argparse
import re
import struct
import sys
from pathlib import Path

LIME = ("#D9F05B", "#EEF6C8", "#EEF8C2", "var(--mark)", "var(--mark-soft)")
KANA = re.compile(r"[぀-ヿ]")
# 簡体字にしかない字（日本語の文章にはまず出ない）
SIMPLIFIED = set("这们说图题问还进对时为发过样么个见读讲则关审议选设计产应让谁钱较层环节线车门间实现单页阶")
TEXT_RE = re.compile(r"<text\b[^>]*>(.*?)</text>", re.S)
TAG_RE = re.compile(r"<[^>]+>")


HIDDEN = re.compile(r'class="[^"]*\b(?:eyebrow|ey|hd|title)\b')  # PNG では隠れる眉標・長い見出し


def texts(html: str) -> list[str]:
    svg = [TAG_RE.sub("", m.group(2)).strip() for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", html, re.S)
           if not HIDDEN.search(m.group(1))]
    body = re.sub(r"<(script|style|svg|title|desc)\b.*?</\1>", " ", html, flags=re.S)
    plain = [t.strip() for t in TAG_RE.sub("\n", body).split("\n")]
    return [t for t in svg + plain if t]


def h1_mark(html: str) -> str:
    m = re.search(r"<h[12][^>]*>(?:(?!</h[12]>).)*?<mark>(.*?)</mark>", html, re.S)
    return TAG_RE.sub("", m.group(1)) if m else ""


def _num(attrs: str, k: str) -> float:
    m = re.search(rf'\b{k}="(-?[\d.]+)"', attrs)
    return float(m.group(1)) if m else 0.0


def _box(tag: str, attrs: str) -> tuple[float, float, float, float] | None:
    if tag == "rect":
        x, y, w, h = (_num(attrs, k) for k in ("x", "y", "width", "height"))
        return (x, y, x + w, y + h) if w > 40 and h > 20 else None  # 凡例の色見本は除く
    if tag == "circle":
        cx, cy, r = (_num(attrs, k) for k in ("cx", "cy", "r"))
        return (cx - r, cy - r, cx + r, cy + r) if r > 20 else None
    if tag == "polygon":
        pts = [float(v) for v in re.findall(r"-?[\d.]+", re.search(r'points="([^"]*)"', attrs).group(1))]
        xs, ys = pts[0::2], pts[1::2]
        return (min(xs), min(ys), max(xs), max(ys)) if max(xs) - min(xs) > 40 else None
    return None


def lime_texts(html: str) -> list[str]:
    """莱姆で塗った図形ごとに、その範囲内に置かれた文字をまとめて返す（変形は考慮しない）。"""
    svg_texts = [(_num(m.group(1), "x"), _num(m.group(1), "y"), TAG_RE.sub("", m.group(2)))
                 for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", html, re.S)]
    out = []
    for m in re.finditer(r"<(rect|polygon|circle)\b([^>]*)>", html):
        if not any(f'fill="{c}"' in m.group(2) for c in LIME):
            continue
        box = _box(m.group(1), m.group(2))
        if box:
            out.append(" ".join(t for x, y, t in svg_texts if box[0] <= x <= box[2] and box[1] <= y <= box[3]))
    out += [TAG_RE.sub("", t) for t in re.findall(r'class="[^"]*\b(?:hot|lime)\b[^"]*"[^>]*>(.*?)</div>', html, re.S)]
    return out


def bigrams(s: str) -> set[str]:
    s = re.sub(r"\s", "", s)
    return {s[i:i + 2] for i in range(len(s) - 1)}


def png_width(p: Path) -> int:
    with p.open("rb") as f:
        head = f.read(24)
    return struct.unpack(">I", head[16:20])[0] if head[:8] == b"\x89PNG\r\n\x1a\n" else 0


def shape_counts(html: str) -> tuple[int, int]:
    svg = re.sub(r"<defs>.*?</defs>|<g class=\"wp-badges.*?<!--/wp-badges-->", "", html, flags=re.S)
    diamonds = len(re.findall(r"<polygon points=\"[\d.]+,[\d.]+ [\d.]+,[\d.]+ [\d.]+,[\d.]+ [\d.]+,[\d.]+\"", svg))
    cards = len(re.findall(r"<rect\b[^>]*width=\"(?:[5-9]\d|\d{3,})", svg))
    return diamonds, cards


def sections(p: Path) -> list[tuple[str, str]]:
    """1ファイル1図。frames.html のように <section class="f"> が並ぶときは1枚ずつに分ける。リンクした CSS も含める。"""
    html = p.read_text(encoding="utf-8")
    css = "".join((p.parent / h).read_text(encoding="utf-8") for h in re.findall(r'<link[^>]*href="([^":]+\.css)"', html)
                  if (p.parent / h).exists())
    parts = re.findall(r'<section\b[^>]*id="([^"]+)"[^>]*>(.*?)</section>', html, re.S)
    if len(parts) < 2:
        return [(p.name, html + css)]
    return [(f"{p.name}#{sid}", body + css) for sid, body in parts]


def lint_file(name: str, html: str, article: str, lang: str, source: Path | None) -> tuple[list[str], list[str]]:
    errs, warns = [], []
    mark = h1_mark(html)
    limes = [t for t in lime_texts(html) if t.strip()]
    if mark and limes and not any(bigrams(mark) & bigrams(t) for t in limes):
        warns.append(f"焦点が2つかも：見出し「{mark}」と図内の莱姆「{limes[0][:16]}」が別の語（同じ讯息でなければ片方を外す）")
    ffs = re.findall(r"font-feature-settings\s*:\s*([^;}]+)", html)
    if lang == "zh" and ffs and "palt" in ffs[-1]:  # 後から normal で上書きしていれば可
        errs.append('palt：中国語の図では font-feature-settings を normal に')
    ts = texts(html)
    if lang == "ja":
        bad = [t for t in ts if not KANA.search(t) and (set(t) & SIMPLIFIED)]
        if bad:
            errs.append("中国語残り：" + " / ".join(b[:16] for b in bad[:4]))
    if article:
        nums = {n for t in ts for n in re.findall(r"\d+(?:\.\d+)?", t)} - {"0", "1", "2", "3", "4", "5"}
        words = {w for t in ts for w in re.findall(r"[A-Za-z][A-Za-z.+-]{2,}", t)}
        miss = sorted(x for x in nums | words if x not in article and x.lower() not in article.lower())
        if miss:
            warns.append("本文にない：" + ", ".join(miss[:8]))
    if source:
        sp = source / name
        if sp.exists():
            a, b = shape_counts(html), shape_counts(sp.read_text(encoding="utf-8"))
            if a[0] != b[0] or abs(a[1] - b[1]) > 2:
                warns.append(f"構造の差：菱形 {a[0]} vs 原文 {b[0]}、カード {a[1]} vs 原文 {b[1]}")
    return errs, warns


def detect_lang(article: str) -> str:
    return "ja" if len(KANA.findall(article)) > 200 else "zh"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", type=Path)
    ap.add_argument("--article", type=Path)
    ap.add_argument("--source", type=Path, help="翻訳版のとき、原文版の diagrams ディレクトリ")
    a = ap.parse_args()
    art_path = a.article or next((p for p in (a.dir.parent.parent / "article.md", a.dir.parent / "article.md") if p.exists()), None)
    article = art_path.read_text(encoding="utf-8") if art_path else ""
    lang = detect_lang(article) if article else ("ja" if "ja" in a.dir.parts else "zh")
    files = sorted(a.dir.glob("[0-9]*.html")) or sorted(a.dir.glob("frames.html"))
    used = {Path(r).stem for r in re.findall(r"\]\(([^)]+\.png)\)", article)}
    if used and any(p.stem in used for p in files):
        files = [p for p in files if p.stem in used]  # 本文が使っている図だけ
    n_err = 0
    for p in files:
        for name, html in sections(p):
            errs, warns = lint_file(name, html, article, lang, a.source)
            for e in errs:
                print(f"  × {name}: {e}")
            for w in warns:
                print(f"  ! {name}: {w}")
            n_err += len(errs)
    if art_path:
        for rel in re.findall(r"\]\(([^)]*screenshots/[^)]+\.png)\)", article):
            img = art_path.parent / rel
            if img.exists() and png_width(img) > 2400:
                print(f"  ! {rel}: 幅 {png_width(img)}px（UI の截圖なら要所を切り出し、番号ラベルを付ける）")
    print("lint OK" if not n_err else f"  × lint：{n_err} 件（未完成扱い）")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
