"""知識圖解・説明型配図を warm-paper 標準で仕上げる一括コマンド。

使い方: python3 warm-paper-build.py <diagrams_dir> [file.html ...]
順番: 1) pdm-flat 配色なら warm-paper へ変換 → 2) 仕上げ（polish）→ 3) badges.json があればバッジ → 4) PNG 書き出し → 5) 見出しの長さチェック → 6) バッジの抜け → 7) figure-lint
対象ファイルを省略すると <diagrams_dir>/[0-9]*.html 全部。再実行しても結果は同じ。
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TITLE_MAX = 16  # 見出しの上限（全角換算の文字数）


def load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def title_len(html: str) -> tuple[str, float]:
    t = re.sub(r"<[^>]+>", "", re.search(r"<h1>(.*?)</h1>", html, re.S).group(1))
    return t, sum(0.5 if ord(c) < 128 else 1 for c in t)


def main() -> None:
    root = Path(sys.argv[1])
    files = [root / f for f in sys.argv[2:]] or sorted(root.glob("[0-9]*.html"))
    convert, polish = load("warm-paper-convert"), load("warm-paper-polish")
    badges, shoot = load("warm-paper-badges"), load("warm-paper-shoot")
    for p in files:
        s = p.read_text(encoding="utf-8")
        if is_pdm_flat(s):
            s = convert.convert(s)
        p.write_text(polish.polish(s), encoding="utf-8")
    if (root / "badges.json").exists():
        badges.run(root / "badges.json")
    warnings, spacing_bad = [], []
    for p in files:
        if not shoot.shoot(str(p)):
            spacing_bad.append(p.name)
        t, n = title_len(p.read_text(encoding="utf-8"))
        if n > TITLE_MAX:
            warnings.append(f"  ! 見出しが長い（{n:g} > {TITLE_MAX}）: {p.name}「{t}」")
    print("\n".join(warnings) or "見出しの長さ OK")
    # 引数で渡していない既存図も含め、フォルダ全体の配色を検査する（流用した旧図の pdm-flat 残りを止める）
    stale = [p.name for p in sorted(root.glob("[0-9]*.html")) if is_pdm_flat(p.read_text(encoding="utf-8"))]
    if stale:
        print("  × warm-paper 未変換の図があります（引数なしで再実行すると変換されます）: " + ", ".join(stale))
        sys.exit(1)
    print("フォルダ全体の配色 OK（warm-paper）")
    if spacing_bad:
        # 文字サイズは下げられない（最小 16）ので、文言を短くする・行を分ける・枠を広げるで直してから再実行
        print("  × 間隔の問題が残っています（未完成扱い）: " + ", ".join(spacing_bad))
        sys.exit(1)
    print("間隔 OK（重なり・はみ出しなし）")
    if badges.SKIPPED:
        # 黙って抜けると審図まで気づかない（2026-10-26：08 の菱形のアイコンが抜けたままだった）。
        # badges.json で cx/cy を指定するか、anchor を置ける文字に変えて再実行
        print("  × バッジを置けなかった（cx/cy で位置を指定）: " + ", ".join(badges.SKIPPED))
        sys.exit(1)
    # 審図で毎回出た指摘（莱姆の焦点・palt・訳し残し・本文にない語）を機械で先に拾う
    sys.stdout.flush()
    lint = subprocess.run([sys.executable, str(HERE / "figure-lint.py"), str(root)])
    if lint.returncode:
        sys.exit(1)


def is_pdm_flat(html: str) -> bool:
    return "#3157d5" in html.lower() or "--paper:#ffffff" in html.lower()


if __name__ == "__main__":
    main()
