#!/usr/bin/env bash
# Links every skill in this repo into Claude Code and Codex, and sets up your
# private personal folder. Run again any time; `git pull` then updates all projects.
#   ./install.sh          link (recommended, updates with git pull)
#   ./install.sh --copy   copy instead of link
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:-link}"
TARGETS=("$HOME/.claude/skills" "$HOME/.codex/skills")
PERSONAL="$HOME/.ai-skills/personal"

for target in "${TARGETS[@]}"; do
  mkdir -p "$target"
  for dir in "$REPO"/skills/*/; do
    name="$(basename "$dir")"
    [ "$name" = "_template" ] && continue
    dest="$target/$name"
    if [ -e "$dest" ] && [ ! -L "$dest" ]; then
      echo "skip  $dest (a real folder is already there; move it to install this one)"
      continue
    fi
    rm -f "$dest"
    if [ "$MODE" = "--copy" ]; then cp -R "${dir%/}" "$dest"; else ln -s "${dir%/}" "$dest"; fi
    echo "ok    $dest"
  done
done

if [ ! -e "$PERSONAL/taste.md" ]; then
  mkdir -p "$PERSONAL/styles"
  cp "$REPO/skills/design-kit/personal-template/taste.md" "$PERSONAL/taste.md"
  echo "made  $PERSONAL/taste.md (private, edit it to set your taste)"
else
  echo "keep  $PERSONAL/taste.md (already set up)"
fi
