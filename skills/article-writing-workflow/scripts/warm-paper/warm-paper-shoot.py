"""warm-paper の図 HTML を PNG に書き出す（見出し＋SVG、幅 1360px @2x、高さは中身に合わせる）。

使い方: python3 warm-paper-shoot.py <file.html>...
"""
import html
import math
import os
import re
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WIDTH, PAD, CONTENT_W = 1360, 48, 1232
TITLE_PX, TITLE_LINE, TITLE_GAP = 36, 47, 20


def chrome(*args: str) -> str:
    cmd = ["perl", "-e", "alarm 60; exec @ARGV", CHROME, "--headless=new", "--disable-gpu",
           "--hide-scrollbars", "--virtual-time-budget=10000", *args]
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def shoot(path: str) -> bool:
    """PNG を書き出す。間隔の問題（重なり・はみ出し・近すぎ）があれば False。"""
    url = f"file://{os.path.abspath(path)}#shot"
    for _ in range(3):  # headless Chrome がたまに空を返すので再試行
        dom = chrome(f"--window-size={WIDTH},900", "--dump-dom", url)
        if "viewBox" in dom:
            break
    m = re.search(r'<svg[^>]*viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"', dom)
    if not m:
        raise SystemExit(f"viewBox not found: {path}")
    w, h = map(float, m.groups())
    mh = re.search(r'data-main-h="([\d.]+)"', dom)
    if mh:
        height = int(PAD * 2 + float(mh.group(1))) + 4
    else:
        title = re.sub(r"<[^>]+>", "", re.search(r"<h1>(.*?)</h1>", dom, re.S).group(1))
        lines = math.ceil(len(title) * TITLE_PX * 1.05 / CONTENT_W)
        height = int(PAD * 2 + lines * TITLE_LINE + TITLE_GAP + CONTENT_W * h / w) + 8
    out = path[:-5] + ".png"
    chrome("--force-device-scale-factor=2", f"--window-size={WIDTH},{height}", f"--screenshot={out}", url)
    print(out, WIDTH, height)
    ov = re.search(r'data-overlap="([^"]+)"', dom)
    if ov:
        print(f"  × 間隔の問題: {os.path.basename(path)}: {html.unescape(ov.group(1))}")
    return not ov


if __name__ == "__main__":
    bad = [p for p in sys.argv[1:] if not shoot(p)]
    sys.exit(1 if bad else 0)
