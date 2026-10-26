#!/usr/bin/env bash
# 上流の diagram-design / yomiyasu を vendor/ へ再コピーする。
# 使い方: ./scripts/sync-vendor.sh   （実行後 vendor/SOURCES.md の版本・日付を更新すること）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/skills/article-writing-workflow/vendor"
# 既定は GitHub から shallow clone。ローカルの clone を使う場合は環境変数で指定する。
DD_REPO="https://github.com/cathrynlavery/diagram-design.git"
YO_REPO="https://github.com/nanaism/yomiyasu.git"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
if [ -z "${DIAGRAM_DESIGN_SRC:-}" ]; then git clone -q --depth 1 "$DD_REPO" "$TMP/diagram-design"; fi
if [ -z "${YOMIYASU_SRC:-}" ]; then git clone -q --depth 1 "$YO_REPO" "$TMP/yomiyasu"; fi
DD_SRC="${DIAGRAM_DESIGN_SRC:-$TMP/diagram-design}"
YO_SRC="${YOMIYASU_SRC:-$TMP/yomiyasu}"
EXCLUDES=(--exclude __pycache__ --exclude .DS_Store)

for src in "$DD_SRC/skills/diagram-design" "$YO_SRC/SKILL.md"; do
  [ -e "$src" ] || { echo "× 上流が見つからない: $src" >&2; exit 1; }
done

rsync -a --delete "${EXCLUDES[@]}" --exclude LICENSE "$DD_SRC/skills/diagram-design/" "$VENDOR/diagram-design/"
cp "$DD_SRC/LICENSE" "$VENDOR/diagram-design/LICENSE"

mkdir -p "$VENDOR/yomiyasu"
rsync -a --delete "${EXCLUDES[@]}" "$YO_SRC/references/" "$VENDOR/yomiyasu/references/"
rsync -a --delete "${EXCLUDES[@]}" "$YO_SRC/scripts/" "$VENDOR/yomiyasu/scripts/"
cp "$YO_SRC/SKILL.md" "$YO_SRC/LICENSE" "$VENDOR/yomiyasu/"

echo "✓ vendor 更新完了"
echo "  diagram-design commit: $(git -C "$DD_SRC" log -1 --format='%h %cs' 2>/dev/null || echo 'git なし')"
echo "  yomiyasu commit: $(git -C "$YO_SRC" log -1 --format='%h %cs' 2>/dev/null || echo 'git なし')"
echo "  vendor/SOURCES.md の版本・复制日期を更新してください"
