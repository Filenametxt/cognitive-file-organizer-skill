#!/usr/bin/env bash
set -euo pipefail

# File Organizer Agent Skills Installer (/fsortcheck & /fsortdump)
# Supports: Unsloth Desktop (Unsloth Studio), Claude Code, OpenAI Codex CLI,
#           Cursor, Google Antigravity, and universal ~/.agents/skills.

REPO_URL="https://github.com/Filenametxt/file-organizer.git"
INSTALL_BASE="${HOME}/.local/share/agent-repos/file-organizer"

# Determine source directory (if running from cloned checkout vs curl pipe)
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

if [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/skills/fsortcheck" ]; then
  SOURCE_DIR="$SCRIPT_DIR"
else
  echo "==> Cloning file-organizer into ${INSTALL_BASE}..."
  mkdir -p "$(dirname "$INSTALL_BASE")"
  if [ -d "$INSTALL_BASE/.git" ]; then
    git -C "$INSTALL_BASE" pull --ff-only
  else
    git clone "$REPO_URL" "$INSTALL_BASE"
  fi
  SOURCE_DIR="$INSTALL_BASE"
fi

chmod +x "$SOURCE_DIR/skills/fsortcheck/scripts/organizer_helper.py" \
         "$SOURCE_DIR/skills/fsortdump/scripts/organizer_helper.py"

# 1. Universal Agent Skills directory (~/.agents/skills) — read natively by Unsloth Desktop
mkdir -p "${HOME}/.agents/skills"
ln -sfn "${SOURCE_DIR}/skills/fsortcheck" "${HOME}/.agents/skills/fsortcheck"
ln -sfn "${SOURCE_DIR}/skills/fsortdump"  "${HOME}/.agents/skills/fsortdump"
echo "✓ Installed into ~/.agents/skills (Unsloth Desktop / Universal Agent Skills)"

# 2. Unsloth Desktop mirror (~/.unsloth/skills) if ~/.unsloth exists
if [ -d "${HOME}/.unsloth" ]; then
  if [ ! -e "${HOME}/.unsloth/skills" ]; then
    ln -s "${HOME}/.agents/skills" "${HOME}/.unsloth/skills"
  elif [ -d "${HOME}/.unsloth/skills" ] && [ ! -L "${HOME}/.unsloth/skills" ]; then
    ln -sfn "${SOURCE_DIR}/skills/fsortcheck" "${HOME}/.unsloth/skills/fsortcheck"
    ln -sfn "${SOURCE_DIR}/skills/fsortdump"  "${HOME}/.unsloth/skills/fsortdump"
  fi
  echo "✓ Synced with ~/.unsloth/skills"
fi

# 3. Claude Code (~/.claude/skills) — only when ~/.unsloth is not present (avoids shadowed entries in Unsloth UI) or if --claude is passed
if [ "${1:-}" = "--claude" ] || { [ -d "${HOME}/.claude" ] && [ ! -d "${HOME}/.unsloth" ]; }; then
  mkdir -p "${HOME}/.claude/skills"
  ln -sfn "${SOURCE_DIR}/skills/fsortcheck" "${HOME}/.claude/skills/fsortcheck"
  ln -sfn "${SOURCE_DIR}/skills/fsortdump"  "${HOME}/.claude/skills/fsortdump"
  echo "✓ Installed into ~/.claude/skills (Claude Code)"
fi

# 4. OpenAI Codex CLI (~/.codex/skills)
if [ -d "${HOME}/.codex" ]; then
  mkdir -p "${HOME}/.codex/skills"
  ln -sfn "${SOURCE_DIR}/skills/fsortcheck" "${HOME}/.codex/skills/fsortcheck"
  ln -sfn "${SOURCE_DIR}/skills/fsortdump"  "${HOME}/.codex/skills/fsortdump"
  echo "✓ Installed into ~/.codex/skills (Codex CLI)"
fi

# 5. Google Antigravity CLI (~/.gemini/antigravity-cli/skills)
if [ -d "${HOME}/.gemini/antigravity-cli" ]; then
  mkdir -p "${HOME}/.gemini/antigravity-cli/skills"
  ln -sfn "${SOURCE_DIR}/skills/fsortcheck" "${HOME}/.gemini/antigravity-cli/skills/fsortcheck"
  ln -sfn "${SOURCE_DIR}/skills/fsortdump"  "${HOME}/.gemini/antigravity-cli/skills/fsortdump"
  echo "✓ Installed into ~/.gemini/antigravity-cli/skills (Antigravity)"
fi

echo ""
echo "Installation complete! Available slash commands:"
echo "  /fsortcheck — Cognitive filesystem restructuring (Miller's Law: 7 ± 2)"
echo "  /fsortdump  — Zero-Remainder inbox/dump folder organizer"
