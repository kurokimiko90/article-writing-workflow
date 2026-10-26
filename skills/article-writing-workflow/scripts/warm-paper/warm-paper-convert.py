"""pdm-flat の diagram-design HTML を warm-paper スキンへ変換する。"""
import re
import sys
from pathlib import Path

FONT_LINK = ('<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900'
             '&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">')

ROOT_VARS = """:root {
  --paper:#F6F2EA; --paper-2:#EFE9DD; --card:#FFFCF6; --ink:#1F2A27; --muted:#5E6B66; --soft:#8E948D;
  --rule:rgba(31,42,39,0.12); --rule-solid:#E6DFD2; --accent:#11645B; --accent-tint:#EEF6C8; --link:#0E5048;
  --mark:#D9F05B; --mark-soft:#EEF6C8; --apricot:#F2A97E;
  --sans:'Noto Sans SC','PingFang SC','Hiragino Sans GB',system-ui,sans-serif;
  --serif:var(--sans);
  --mono:'Geist Mono','Noto Sans SC',ui-monospace,monospace;
}"""

EXTRA_CSS = """
body { background:#F6F2EA; position:relative; }
body::before { content:""; position:fixed; inset:0; pointer-events:none; z-index:-1;
  background:radial-gradient(60% 70% at 100% 0%, rgba(242,169,126,.28), transparent 70%),
             radial-gradient(55% 60% at 0% 100%, rgba(217,240,91,.30), transparent 70%); }
body::after { content:""; position:fixed; inset:0; pointer-events:none; opacity:.35; mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0.3 0 0 0 0 0.28 0 0 0 0 0.25 0 0 0 .12 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }
.frame h1 { font-family:var(--sans); font-weight:900; font-size:38px; line-height:1.3; letter-spacing:.03em; margin-bottom:1.25rem; }
.frame h1 mark { background:linear-gradient(transparent 52%, var(--mark) 52%, var(--mark) 92%, transparent 92%); color:inherit; padding:0 .08em; }
body.shot { padding:48px 64px; }
body.shot .eyebrow, body.shot .deck, body.shot .foot { display:none; }
"""

SHADOW_DEFS = ('<filter id="wp-shadow" x="-10%" y="-10%" width="120%" height="140%">'
               '<feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#5a4a32" flood-opacity=".10"/></filter>')

HEX_MAP = {
    "#667085": "#7D857F", "#111a2e": "#1F2A27", "#2a46b0": "#0E5048",
    "#e8ecf3": "#E6DFD2", "#f4f6fa": "#EFE9DD", "#8792a3": "#8E948D",
    "#e7edff": "#EEF6C8", "#3157d5": "#11645B", "#ffffff": "#FFFCF6",
}


def mark_title(m: re.Match) -> str:
    """見出しの後半（最初の区切り記号以降）を蛍光ペンで強調する。"""
    t = m.group(1)
    for sep in ("：", "；", "，"):
        i = t.find(sep)
        if 0 < i < len(t) - 1:
            return f"<h1>{t[:i + 1]}<mark>{t[i + 1:]}</mark></h1>"
    return m.group(0)


def convert(src: str) -> str:
    s = re.sub(r'<link href="https://fonts.googleapis.com[^"]*" rel="stylesheet">', FONT_LINK, src, count=1)
    s = re.sub(r":root\s*\{[^}]*\}", ROOT_VARS, s, count=1)
    s = s.replace("</style>", EXTRA_CSS + "</style>", 1)
    s = s.replace("font:italic 400 16px var(--serif)", "font:500 16px var(--sans)")
    s = re.sub(r"<h1>(.*?)</h1>", mark_title, s, count=1)
    # 重点框：薄緑底＋ライム線
    s = re.sub(r'(<rect[^>]*fill="#e7edff"[^>]*)stroke="#3157d5"', r'\1stroke="#C3DB3E"', s)
    # ノード：濃い枠線を消し、角丸＋柔らかい影
    s = re.sub(r'<rect([^>]*?)rx="6"([^>]*?)stroke="#111a2e" stroke-width="1"',
               r'<rect\1rx="14"\2stroke="rgba(31,42,39,0.08)" stroke-width="1" filter="url(#wp-shadow)"', s)
    s = re.sub(r'(<rect[^>]*?)rx="6"', r'\1rx="14"', s)
    # 全面背景 rect は透明にして暖紙色を透かす
    s = re.sub(r'<rect width="([\d%]+)" height="([\d%]+)" fill="#ffffff"/>', r'<rect width="\1" height="\2" fill="none"/>', s)
    s = s.replace("蓝色 = ", "绿色 = ")
    for old, new in HEX_MAP.items():
        s = s.replace(old, new)
    s = s.replace("rgba(17,26,46,", "rgba(31,42,39,").replace("rgba(102,112,133,", "rgba(125,133,127,")
    s = s.replace("<defs>", "<defs>\n  " + SHADOW_DEFS, 1)
    s = s.replace("</body>",
                  "<script>if(location.hash==='#shot')document.body.classList.add('shot');</script>\n</body>", 1)
    return s


if __name__ == "__main__":
    for p in map(Path, sys.argv[1:]):
        p.write_text(convert(p.read_text(encoding="utf-8")), encoding="utf-8")
        print("converted", p.name)
