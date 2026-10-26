#!/usr/bin/env bash
# article-writing-workflow を対象プロジェクトへ symlink でインストールする。
# 使い方: ./install.sh <対象プロジェクトのパス>
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:?使い方: ./install.sh <対象プロジェクトのパス>}"
DEST="$(cd "$DEST" && pwd)"

link() {
  local target="$1" path="$2"
  mkdir -p "$(dirname "$path")"
  if [ -e "$path" ] && [ ! -L "$path" ]; then
    echo "× 既存の実ファイルがあるためスキップ: $path" >&2
    return
  fi
  ln -sfn "$target" "$path"
  echo "✓ $path -> $target"
}

# Claude Code
link "$SRC/skills/article-writing-workflow" "$DEST/.claude/skills/article-writing-workflow"
link "$SRC/skills/article-figures" "$DEST/.claude/skills/article-figures"
link "$SRC/agents/claude/article-knowledge-editor.md" "$DEST/.claude/agents/article-knowledge-editor.md"
link "../skills/article-writing-workflow/agents/figure-reviewer.md" "$DEST/.claude/agents/article-figure-reviewer.md"

# Codex
link "../../.claude/skills/article-writing-workflow" "$DEST/.agents/skills/article-writing-workflow"
link "$SRC/agents/codex/article-knowledge-editor.toml" "$DEST/.codex/agents/article-knowledge-editor.toml"

# diagram-design 用 warm-paper profile（全プロジェクト共通）
for f in "$SRC"/skills/article-writing-workflow/scripts/warm-paper/warm-paper*; do
  link "$f" "$HOME/.diagram-design/profiles/$(basename "$f")"
done
