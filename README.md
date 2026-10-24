# File Organizer — AI Agent Skills (`fsortcheck` & `fsortdump`)

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-SKILL.md-blue)](https://github.com/Filenametxt/file-organizer)
[![Tested on Unsloth Desktop](https://img.shields.io/badge/Tested_on-Unsloth_Desktop-2ea44f)](https://unsloth.ai)
[![MCP Ready](https://img.shields.io/badge/MCP-Local_%7C_Nextcloud_%7C_Cloud-orange)](https://modelcontextprotocol.io)
[![SkillSpector SAFE](https://img.shields.io/badge/NVIDIA_SkillSpector-SAFE-76b900)](https://github.com/NVIDIA/SkillSpector)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Autonomous, move-only **AI Agent Skills** that organize your **local folders** or **cloud storage (Nextcloud, WebDAV, Google Drive via MCP)** using **Miller's Law ($7 \pm 2$ items per folder)** and **self-documenting `README.md` indexes**.

> **Tested on [Unsloth Desktop](https://unsloth.ai)** with local GGUF models and compatible with **Claude Code, Cursor, OpenAI Codex, Google Antigravity, Windsurf, Cline, and OpenCode**.

---

## 1. The Two Commands

| Skill | Purpose | When to Use |
|---|---|---|
| **`fsortcheck`** | **Full Archive Restructuring** | Organizes your folders to keep **5–9 items per folder** (Miller's Law) and writes a `README.md` guide in each subfolder. |
| **`fsortdump`** | **Inbox / Dump Zero-Remainder** | Empties a transit folder (`Upload`, `Downloads`, `Inbox`) by moving every file and subfolder into your main categories. |

---

## 2. Five Safety & Cognitive Rules

1. **Miller's Law ($7 \pm 2$)**: Keeps **5 to 9 items** per directory. Overloaded folders ($>9$ items) are split into logical subfolders.
2. **Move-Only (Never Deletes Files)**: Files are **only moved (`move_file`)**, never deleted—except verified byte-for-byte duplicates sharing the **exact same SHA-256 hash**.
3. **Protects Code Projects**: Detects programming projects (`Cargo.toml`, `package.json`, `pyproject.toml`, `go.mod`, `.git`, etc.) and moves them as **intact atomic units** without touching internal files.
4. **Self-Documenting `README.md`**: Places a short `README.md` in every organized subfolder so future LLMs know what belongs inside without re-reading every file.
5. **Smart Inspection & Re-Check**: Learns unreadable binary formats (`.docx`, `.zip`) to avoid wasted tool calls, and always re-verifies folders with `list_files` before finishing.

---

## 3. How It Works

```text
  [1. Scan Target] ──► Local Filesystem (Bash) OR Cloud Storage (MCP: Nextcloud, Drive)
         │
         ▼
  [2. Align Categories] ──► Match your mental model (e.g. Personal, University, Finance, Projects)
         │
         ▼
  [3. Move & Balance (7 ± 2)] ──► Keep 5–9 items/folder · Protect code projects · Move-only
         │
         ▼
  [4. Document & Verify] ──► Write subfolder README.md · Re-check with list_files
```

---

## 4. Quick Installation

### Automatic Install (Unsloth Desktop, Claude, Cursor, Codex, Antigravity)
```bash
git clone https://github.com/Filenametxt/file-organizer.git ~/.local/share/agent-repos/file-organizer
~/.local/share/agent-repos/file-organizer/install.sh
```

### Or via `npx skills`
```bash
npx skills add Filenametxt/file-organizer
```

---

## 5. How to Use (2 Golden Rules)

When prompting the agent, always specify two things:
1. **Where to work**: tell the agent whether to use your **Cloud MCP server** (e.g., Nextcloud MCP) or **local filesystem tools** (e.g., `~/Documents`).
2. **Your Categories**: list the main top-level folders you want to use.

### Copy-Paste Prompts

**Full reorganization (`fsortcheck`):**
```text
@fsortcheck Use my Nextcloud MCP tools. Reorganize my workspace into these categories: [Personal, University, Finance, Projects].
```

**Empty an inbox/dump folder (`fsortdump`):**
```text
@fsortdump Use my Nextcloud MCP tools to empty the "Upload" folder and move all files and subfolders into [Personal, University, Finance, Projects].
```

**Local folder reorganization:**
```text
@fsortcheck Reorganize my local folder ~/Documents using local filesystem tools into [Work, Personal, Finance, Projects].
```

---

## 6. Agent Trigger Reference

| AI Agent / IDE | How to Trigger | Skill Path |
|---|---|---|
| **Unsloth Desktop (Unsloth Studio)** | **`@fsortcheck`** / **`@fsortdump`** | `~/.agents/skills/` |
| **Claude Code / Cursor** | **`/fsortcheck`** / **`/fsortdump`** | `~/.claude/skills/` · `~/.cursor/skills/` |
| **OpenAI Codex CLI** | **`/fsortcheck`** / **`$fsortcheck`** | `~/.codex/skills/` |
| **Google Antigravity** | Mention **`fsortcheck`** / **`fsortdump`** | `~/.gemini/antigravity-cli/skills/` |

---

## License

[MIT License](LICENSE) · Created by [@Filenametxt](https://github.com/Filenametxt)
