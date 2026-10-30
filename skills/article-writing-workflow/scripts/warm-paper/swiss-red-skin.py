"""warm-paper の図を「swiss-red」（C 方案・瑞士式の大きな文字）スキンに変換して PNG を書き出す。

使い方: python3 swiss-red-skin.py <warm-paper の diagrams_dir> <出力 dir> [--article article.md]
  --article を渡すと、本文が参照する図だけを処理する。元の図（入力側）は書き換えない。

規則（swiss-red.md と同じ。2026-10-30 独立審図 S2–S6 から）:
  - 線・矢印・アイコン・人物は墨 #0A0A0A。矢印は 3px、白カードは 2px 墨枠。灰色の矢印は使わない。
  - 朱红 #FF3B1F は焦点だけ：見出しのキーワード、warm-paper で莱姆だった要素、焦点枠（旧 #EEF6C8）の中の強調文字。
    旧青緑（accent）は焦点ではないので墨にする（2026-10-30 審図：標題の赤と図内の赤が別の事を指していた）。
  - 文字の最も淡い色は #6B6B6B（#999 は使わない）。
  - 投影・纹理・胶带・カードの回転は消す。見出しは 56px／weight 800、font-synthesis:none、下に 8px の墨線。
"""
import argparse
import re
import subprocess
import sys
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
INK, RED, TINT = "0A0A0A", "FF3B1F", "FFE7E1"

NEUTRAL = {  # 文字・図形で共通
    "F3F1EC": "F4F3EE", "F6F2EA": "F4F3EE", "FFFCF6": "FFFFFF", "F7F5F0": "FFFFFF", "F4EFE6": "FFFFFF",
    "E8E5DE": "E4E1D8", "EFE9DD": "E4E1D8", "DAD6CD": "CFCCC3", "DAD4C8": "CFCCC3", "D9D3C4": "CFCCC3",
    "E6DFD2": "CFCCC3", "E8E3D6": "CFCCC3", "E4D9BC": "CFCCC3", "CFCBC2": "CFCCC3", "D3DCE2": "CFCCC3",
    "E4EAEE": "EEEDE8", "EDF1F3": "EEEDE8", "DCE6EE": "EEEDE8", "E7F0EC": "EEEDE8",
    "F6E7A8": "FFFFFF", "E3D49A": "CFCCC3", "FCEFE4": "FFFFFF",
}
SHAPE = {**NEUTRAL, **{k: INK for k in ("1F2A27", "3E4A46", "2F4858", "5C6670", "7D857F", "5E6B66", "8E948D",
                                        "9AA09A", "11645B", "0E5048", "8FA3B0")},
         "D9F05B": RED, "C3DB3E": RED, "D9E39A": RED, "EEF6C8": TINT, "E6EFD9": TINT, "F2A97E": "CFCCC3"}
TEXT = {**NEUTRAL, "1F2A27": INK, "3E4A46": INK, "2F4858": INK, "11645B": INK, "0E5048": INK,
        "5E6B66": "4A4A4A", "5C6670": "4A4A4A", "F2A97E": "4A4A4A",
        "7D857F": "6B6B6B", "8E948D": "6B6B6B", "9AA09A": "6B6B6B", "8FA3B0": "6B6B6B",
        "D9F05B": RED, "C3DB3E": RED}
ACCENT = {"11645B", "0E5048"}
FOCAL_FILL = ("#EEF6C8", "#D9F05B", "#E6EFD9")
RGBA = {"31,42,39": "10,10,10", "47,72,88": "10,10,10", "125,133,127": "10,10,10",
        "232,229,222": "228,225,216", "238,246,200": "255,231,225"}

CSS = """<style>/* skin:swiss-red */
:root{--hand:'Hiragino Sans','Noto Sans JP','PingFang SC',sans-serif!important;--serif:var(--sans)!important}
body,body.shot{background:#F4F3EE!important}body::before,body::after{display:none!important}
svg text,body{font-synthesis:none}
.frame h1{color:#0A0A0A!important;font-weight:800!important;font-size:56px!important;line-height:1.2!important;
  letter-spacing:.02em!important;font-synthesis:none;border-bottom:8px solid #0A0A0A;padding-bottom:14px;margin-bottom:28px!important}
body>h1{color:#0A0A0A!important;font-weight:800!important;font-size:42px!important;font-synthesis:none;
  border-bottom:6px solid #0A0A0A;padding-bottom:6px}
html body h1 mark,html body .frame h1 mark,html body .frame h1 mark *{background:none!important;color:#FF3B1F!important;padding:0!important}
</style>
"""


def grey(h: str, floor: int | None = None) -> str:
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    v = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
    if floor is not None:
        v = min(v, floor)  # 文字は #6B6B6B より淡くしない
    return f"{v:02X}" * 3


def num(attrs: str, k: str) -> float:
    m = re.search(rf'\b{k}="(-?[\d.]+)"', attrs)
    return float(m.group(1)) if m else 0.0


def focal_boxes(s: str) -> list[tuple[float, float, float, float]]:
    """warm-paper で焦点枠（薄緑底・莱姆線・莱姆塗り）だった矩形の範囲。"""
    out = []
    for m in re.finditer(r"<rect\b([^>]*)>", s):
        a = m.group(1).upper()
        if any(f'FILL="{c}"' in a for c in FOCAL_FILL) or 'STROKE="#C3DB3E"' in a:
            x, y, w, h = (num(m.group(1), k) for k in ("x", "y", "width", "height"))
            if w > 40 and h > 20:
                out.append((x, y, x + w, y + h))
    return out


def dark_boxes(s: str) -> list[tuple[float, float, float, float]]:
    """換皮後に墨（黒）で塗られる図形の範囲。中の文字は白にする（2026-10-30 用户：黑底上的字看不清）。"""
    dark = {k for k, v in SHAPE.items() if v == INK}
    out = []
    # path は相対座標で範囲を誤るので対象外（2026-10-30：27 の目盛りの path で文字が白くなった）
    for m in re.finditer(r"<(rect|circle)\b([^>]*)>", s):
        a = m.group(2)
        f = re.search(r'fill\s*[=:]\s*"?#([0-9A-Fa-f]{6})', a)
        if not f or f.group(1).upper() not in dark:
            continue
        op = re.search(r'(?:fill-)?opacity\s*[=:]\s*"?([\d.]+)', a)
        if op and float(op.group(1)) < 0.6:
            continue  # 墨の半透明（薄い地）は黒地ではない（2026-10-30：02 の上段・印章が白文字で消えた）
        if m.group(1) == "rect":
            x, y, w, h = (num(a, k) for k in ("x", "y", "width", "height"))
        else:
            r = num(a, "r"); x, y, w, h = num(a, "cx") - r, num(a, "cy") - r, 2 * r, 2 * r
        if w >= 24 and h >= 18:
            out.append((x, y, x + w, y + h))
    return out


def recolor_tag(tag: str, name: str, boxes, darks=()) -> str:
    is_text = name in ("text", "tspan", "style")
    table = TEXT if is_text else SHAPE
    inside = lambda bs: name in ("text", "tspan") and any(b[0] <= num(tag, "x") <= b[2] and b[1] - 4 <= num(tag, "y") <= b[3] + 4 for b in bs)
    in_focus = inside(boxes)
    on_dark = inside(darks)

    def sub(m: re.Match) -> str:
        h = m.group(1).upper()
        if in_focus and h in ACCENT:
            return "#" + RED  # 焦点枠の中の強調文字だけ朱红
        if h in table:
            return "#" + table[h]
        # 未知色は灰に。style ブロックは背景色の変数も含むので淡さの下限を付けない（2026-10-30：33 の地が暗くなった）
        return "#" + grey(h, 0x6B if name in ("text", "tspan") else None)
    tag = re.sub(r"#([0-9A-Fa-f]{6})\b", sub, tag)
    if on_dark and f"#{RED}" not in tag:
        # 黒地の文字は白。クラスの fill より強い inline style で指定する
        tag = re.sub(r'\sfill="[^"]*"', "", tag)
        tag = re.sub(r"fill\s*:\s*#[0-9A-Fa-f]{6}", "fill:#FFFFFF", tag) if "style=" in tag and "fill:" in tag else \
            (tag.replace('style="', 'style="fill:#FFFFFF;', 1) if "style=" in tag else tag.replace(f"<{name}", f'<{name} style="fill:#FFFFFF"', 1))
    return tag


def strokes(tag: str, name: str) -> str:
    if name in ("line", "path", "polyline") and "marker-end" in tag:
        tag = re.sub(r'stroke-width="([\d.]+)"', lambda m: f'stroke-width="{max(3.0, float(m.group(1))):g}"', tag)
    if name == "rect" and 'fill="#FFFFFF"' in tag and "mask" not in tag and num(tag, "width") >= 60 and num(tag, "height") >= 36:
        tag = re.sub(r'\s(stroke|stroke-width)="[^"]*"', "", tag)
        tag = tag.replace("<rect", '<rect stroke="#0A0A0A" stroke-width="2"', 1)
    return tag


PERSON = re.compile(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)" fill="#2F4858"/>(<path d="M[^"]*q0 -[^"]*z" fill="#8FA3B0"/>)')


def person(m: re.Match) -> str:
    """人物アイコン：頭を肩の上に重ね、地色の輪で首を切る（2026-10-30 用户：黑一团看不出是人）。"""
    cx, cy, r = float(m.group(1)), float(m.group(2)), float(m.group(3))
    body = m.group(4).replace("#8FA3B0", f"#{INK}")
    gap = max(3.0, r * 0.3)
    return (f'{body}<circle cx="{cx:g}" cy="{cy - r * 0.3:.1f}" r="{r:.1f}" fill="#{INK}" '
            f'stroke="#F4F3EE" stroke-width="{gap:.1f}" paint-order="stroke"/>')


def skin(s: str) -> str:
    s = re.sub(r"#([0-9a-fA-F]{3})\b", lambda m: "#" + "".join(c * 2 for c in m.group(1)), s)
    s = PERSON.sub(person, s)
    boxes, darks = focal_boxes(s), dark_boxes(s)
    # style ブロックは文字の色として扱う（クラスの fill はほぼ文字）
    s = re.sub(r"<style\b.*?</style>", lambda m: recolor_tag(m.group(0), "style", []), s, flags=re.S)

    def tag(m: re.Match) -> str:
        t, name = m.group(0), m.group(1).lower()
        if name == "style":
            return t
        t = recolor_tag(t, name, boxes, darks)
        t = re.sub(r'\sfilter="url\(#[^)]*\)"', "", t)          # 投影・纹理
        t = re.sub(r"\s?rotate\([^)]*\)", "", t)                 # 回転
        t = re.sub(r'\stransform="\s*"', "", t)
        return strokes(t, name)
    s = re.sub(r"<([a-zA-Z]+)\b[^>]*>", tag, s)
    for a, b in RGBA.items():
        s = s.replace(f"rgba({a},", f"rgba({b},")
    # 胶带（半透明の小さな矩形）は消す
    s = re.sub(r'<rect\b[^>]*fill-opacity="\.?\d*"[^>]*/>', lambda m: "" if num(m.group(0), "width") <= 90 else m.group(0), s)
    # 見出しが SVG の文字（05 型）なら、「：」の後ろを朱红に
    if "<h1" not in s:
        s = re.sub(r'(<text\b[^>]*font-size="(?:2[8-9]|[3-9]\d)"[^>]*>)([^<：]+：)([^<]+)</text>',
                   r'\1\2<tspan fill="#FF3B1F">\3</tspan></text>', s, count=1)
    return s.replace("</head>", CSS + "</head>", 1) if "</head>" in s else CSS + s


def shoot(p: Path) -> bool:
    html = p.read_text(encoding="utf-8")
    if "wp-crop" in html:
        spec = importlib.util.spec_from_file_location("shoot", HERE / "warm-paper-shoot.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.shoot(str(p))
    # 固定サイズのページ（05・33 型）は body の幅・高さで撮る（2026-10-30：33 が 800px で切れた）
    m = re.search(r"body\s*\{[^}]*?width:(\d+)px;[^}]*?height:(\d+)px", html)
    w, h = (int(m.group(1)), int(m.group(2))) if m else (1360, 900)
    subprocess.run(["perl", "-e", "alarm 60; exec @ARGV", CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size={w},{h}", f"--screenshot={p.with_suffix('.png')}",
                    f"file://{p}"], capture_output=True)
    print(p.with_suffix(".png"), w, h)
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--article", type=Path)
    a = ap.parse_args()
    files = sorted(a.src.glob("[0-9]*.html"))
    if a.article:
        used = set(re.findall(r"diagrams[^/]*/([^)/]+)\.png", a.article.read_text(encoding="utf-8")))
        files = [f for f in files if f.stem in used]
    a.out.mkdir(parents=True, exist_ok=True)
    bad = []
    for f in files:
        p = (a.out / f.name).resolve()
        p.write_text(skin(f.read_text(encoding="utf-8")), encoding="utf-8")
        if not shoot(p):
            bad.append(f.name)
    print("間隔 OK" if not bad else "  × 間隔の問題: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
