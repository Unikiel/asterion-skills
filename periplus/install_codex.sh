#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "Usage: bash install_codex.sh ./periplus-skill-v2.4.0.zip"; exit 2; fi
zipfile="$1"
if [ ! -f "$zipfile" ]; then echo "ZIP not found: $zipfile"; exit 2; fi
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
unzip -q "$zipfile" -d "$tmp"
if [ ! -f "$tmp/periplus/SKILL.md" ]; then echo 'Invalid ZIP: missing periplus/SKILL.md'; exit 2; fi
dest="$HOME/.codex/skills/periplus"
mkdir -p "$(dirname "$dest")"
if [ -d "$dest" ]; then backup="${dest}.backup-$(date +%Y%m%d-%H%M%S)"; mv "$dest" "$backup"; echo "Backup: $backup"; fi
cp -R "$tmp/periplus" "$dest"
test -f "$dest/SKILL.md"
echo "Installed Periplus to $dest"
echo 'Restart Codex, then invoke $periplus.'
