# File Organizer — Cognitive AI Agent Skills (`/fsortcheck` & `/fsortdump`)

[![Agent Skills Spec](https://img.shields.io/badge/Agent_Skills-SKILL.md-blue)](https://github.com/Filenametxt/file-organizer)
[![Tested on Unsloth Desktop](https://img.shields.io/badge/Tested_on-Unsloth_Desktop-2ea44f)](https://unsloth.ai)
[![MCP Compatible](https://img.shields.io/badge/MCP-Nextcloud_%7C_Filesystem_%7C_Cloud-orange)](https://modelcontextprotocol.io)
[![Security: SkillSpector SAFE](https://img.shields.io/badge/NVIDIA_SkillSpector-SAFE-76b900)](https://github.com/NVIDIA/SkillSpector)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**File Organizer** is a pair of production-tested **AI Agent Skills** (`/fsortcheck` and `/fsortdump`) that turn any local LLM or coding agent into an autonomous, safety-first **file and cloud storage organizer** powered by **Miller's Law ($7 \pm 2$)** and **self-documenting folder `README.md` indexes**.

It is **100% backend-agnostic**: use it on your **local filesystem** via standard system/bash tools, or on **cloud storage** (such as **Nextcloud**, **WebDAV**, **Google Drive**, or **S3**) via **MCP (Model Context Protocol) servers**.

> **Tested & Verified**: Built and stress-tested on **Unsloth Desktop (Unsloth Studio)** using local quantized GGUF models (`llama.cpp`) connected to a live **Nextcloud MCP server**. Because it follows the open `SKILL.md` standard, it works out of the box across **Unsloth Desktop, Claude Code, OpenAI Codex CLI, Cursor, Google Antigravity, Windsurf, Cline, Roo Code, and OpenCode**.

---

## Table of Contents

- [Why File Organizer?](#why-file-organizer)
- [The Two Commands](#the-two-commands)
  - [`/fsortcheck` — Full Filesystem Cognitive Restructuring](#1-fsortcheck--full-filesystem-cognitive-restructuring)
  - [`/fsortdump` — Zero-Remainder Inbox / Dump Organizer](#2-fsortdump--zero-remainder-inbox--dump-organizer)
- [How It Works (Architecture)](#how-it-works-architecture)
- [Prerequisites & How to Prompt Properly](#prerequisites--how-to-prompt-properly)
  - [1. Specify Where to Work (Local Tooling vs. Cloud MCP Server)](#1-specify-where-to-work-local-tooling-vs-cloud-mcp-server)
  - [2. Specify Your Category Classification (Mental Model)](#2-specify-your-category-classification-mental-model)
- [Installation](#installation)
  - [Option A: Automatic Installer (Unsloth Desktop, Claude, Codex, Antigravity)](#option-a-automatic-installer-unsloth-desktop-claude-codex-antigravity)
  - [Option B: `npx skills` CLI](#option-b-npx-skills-cli)
  - [Option C: Manual Symlink Installation](#option-c-manual-symlink-installation)
- [Helper CLI Utility (`organizer_helper.py`)](#helper-cli-utility-organizer_helperpy)
- [Agent Compatibility Matrix](#agent-compatibility-matrix)
- [Security Audit](#security-audit)
- [License](#license)

---

## Why File Organizer?

Most prompts asking an LLM to "organize my files" fail in practice: models either dump everything into generic folders, hallucinate file paths, get stuck in infinite Chain-of-Thought calculation loops on local models, or silently lose files when a server error occurs.

**File Organizer** solves these problems with six behavioral guarantees:

1. **Miller's Law ($7 \pm 2$ Rule)**: Every folder is structured to hold an optimal **5 to 9 items**. If a directory exceeds **9 items** (`OVERFLOW`), the agent creates semantic or chronological subfolders to reduce human cognitive load.
2. **Atomic Software Project Protection**: Automatically detects programming and code project directories (e.g., **Rust** `Cargo.toml`, **Python** `pyproject.toml`, **Node/TS** `package.json`, **Go** `go.mod`, **C/C++** `CMakeLists.txt` / `Makefile`, `.git/`, etc.) and treats them as **indivisible atomic units**. It will move a whole project folder into `Projects/Rust/` if needed, but will **never** split or corrupt internal source trees (`src/`, `target/`, configs, or project `README.md` files).
3. **Self-Documenting `README.md` in Every Subfolder**: Whenever a folder or subfolder is created or reorganized, the agent writes a concise `README.md` inside it describing its purpose, allowed file types, and routing rules. Future LLM runs read these `README.md` files first to make instant, deterministic placement decisions.
4. **Dynamic Tool-Capability Learning**: The agent inspects file contents to understand context whenever a suitable tool exists. If a file format (e.g., `.docx`, `.zip`, or binary files) lacks a reader tool in the current session, the agent **remembers that extension as unreadable** and skips redundant read calls on subsequent files of the same type—while automatically using new parser tools as soon as you add them in the future.
5. **Move-Only Policy & Exact Hash Deduplication**:
   - **Never deletes user files**: File Organizer is strictly a **move-only (`move_file`)** system. Deleting a user file is strictly forbidden unless it is proven to be an **exact byte-for-byte duplicate with the identical cryptographic hash (SHA-256 / MD5)**. If two files share a name but differ in hash/content, the incoming file is renamed (`_v2`) and moved safely.
   - **Mandatory Pre-Delete & Subfolder Re-Check (`list_files`)**: In WebDAV/Nextcloud MCP servers, directories always report `"size_bytes": 0` even when full of files. The skills forbid trusting `size_bytes: 0` and require calling `list_files` inside every subfolder (`Upload/<subfolder>`) before acting, and **never delete the root dump/inbox folder itself** (`/Upload`, `/Downloads`, `/Inbox`).
   - Strictly Fail-Fast on any server or I/O error (such as `HTTP 404 Not Found`).
6. **Anti-Loop Prompt Engineering for Local LLMs**: Specifically tuned so local quantized models emit direct tool calls (`create_folder`, `move_file`, `write_file`) one folder at a time without getting trapped in endless reasoning monologues.

---

## The Two Commands

### 1. `/fsortcheck` — Full Filesystem Cognitive Restructuring

Scans a target directory tree or cloud drive, aligns with your personal category taxonomy, splits overloaded folders ($> 9$ items) into thematic subfolders according to **Miller's Law ($7 \pm 2$)**, and generates a `README.md` index inside every organized folder and subfolder.

### 2. `/fsortdump` — Zero-Remainder Inbox / Dump Organizer

Processes a transit, inbox, or dump folder (such as `Upload`, `Downloads`, or `Inbox`), analyzes the semantic context of every file and subfolder inside it, consults existing destination `README.md` files, moves all items into their proper destination in the main filesystem, and verifies a **Zero-Remainder state** (`0 files, 0 folders` left in the dump folder).

---

## How It Works (Architecture)

```text
  USER PROMPT (/fsortcheck or /fsortdump)
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ 1. DETECT TARGET & BACKEND                                   │
│    • Local Filesystem (Bash / System Tools)                  │
│    • Cloud Storage via MCP (Nextcloud, WebDAV, Drive, etc.)  │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. SCAN & ALIGN CATEGORIES (MENTAL MODEL)                    │
│    • List directories and count items                        │
│    • Confirm top-level categories (Personal, Work, Finance)  │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. CONTEXT ANALYSIS & TOOL-CAPABILITY LEARNING               │
│    • Read existing folder README.md first                    │
│    • Inspect file contents when a reader tool is available   │
│    • Remember unreadable extensions (.docx, .zip) & skip     │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. APPLY MILLER'S LAW (7 ± 2) & PROTECT CODE PROJECTS        │
│    • Keep 5 to 9 items per folder                            │
│    • Detect codebases (Cargo.toml, package.json, .git, etc.) │
│      and treat them as ATOMIC units (never split internals!) │
│    • If > 9 items (OVERFLOW) -> create thematic subfolders   │
│    • Move files atomically (Strict Fail-Fast on HTTP 404)    │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. SELF-DOCUMENT & VERIFY                                    │
│    • Write README.md in every organized folder & subfolder   │
│    • Certify 0 remaining files in dump folder (/fsortdump)   │
└──────────────────────────────────────────────────────────────┘
```

| Step | Action | Safety & Cognitive Rule |
|---|---|---|
| **1. Scope** | Detect Local FS or Cloud MCP tools | Never act without listing source & destination first |
| **2. Taxonomy** | Align with user categories | Ask user if mental model is not specified |
| **3. Inspect** | Read `README.md` & supported files | Cache unsupported extensions to avoid wasted tool calls |
| **4. Restructure** | Enforce **Miller's Law ($7 \pm 2$)** | Split folders with $> 9$ items; **Fail-Fast** on any error |
| **5. Document** | Write `README.md` in each subfolder | Guides future LLMs & certifies `0` items left in dump |

---

## Prerequisites & How to Prompt Properly

To get the best results from `/fsortcheck` and `/fsortdump`, keep two simple rules in mind when prompting your agent:

### 1. Specify Where to Work (Local Tooling vs. Cloud MCP Server)

Because these skills are storage-agnostic, **always tell the agent which environment and path to operate on**:

- **For Cloud Storage (Nextcloud, WebDAV, Google Drive, etc.)**: Make sure the corresponding **MCP server** is enabled in your client (e.g., Nextcloud MCP in Unsloth Desktop) and mention it in your prompt.
- **For Local Directories**: Make sure your agent has local filesystem / bash tool access enabled and specify the target directory path (e.g., `~/Documents` or `~/Downloads`).

### 2. Specify Your Category Classification (Mental Model)

Tell the agent how you mentally divide your files (your top-level taxonomy), or let `/fsortcheck` ask you before moving folders. Providing your categories upfront makes execution faster and tailored to your workflow.

### How to Trigger the Skills (`@` vs `/`)

Different coding agents use slightly different prefixes to invoke skills:
- **Unsloth Desktop (Unsloth Studio)**: Use **`@fsortcheck`** and **`@fsortdump`** (type `@` in the chat input to autocomplete and preload the skill).
- **Claude Code / Cursor / OpenAI Codex**: Use **`/fsortcheck`** and **`/fsortdump`** (or mention the skill by name).
- **Google Antigravity / Other Agents**: Mention **`fsortcheck`** or **`fsortdump`** directly in your prompt.

#### Example Prompts

**Reorganizing a Nextcloud drive on Unsloth Desktop (`@fsortcheck`):**
```text
@fsortcheck Use my Nextcloud MCP tools. Reorganize my root workspace using these top-level categories: [Personal, University, Finance, Projects, Archive].
```

**Emptying an `Upload` dump folder on Nextcloud (`@fsortdump` / `/fsortdump`):**
```text
@fsortdump Use my Nextcloud MCP tools to empty the "Upload" folder and route all files into my main folders [Personal, University, Finance, Projects] leaving Upload completely empty.
```

**Reorganizing a local directory (`/fsortcheck` or `@fsortcheck`):**
```text
@fsortcheck Reorganize my local folder ~/Documents using local filesystem tools. My main categories are [Work, Personal, Taxes, Side-Projects].
```

---

## Installation

### Option A: Automatic Installer (Unsloth Desktop, Claude, Codex, Antigravity)

Clone the repository and run the installer script. It automatically links `fsortcheck` and `fsortdump` into `~/.agents/skills` (read natively by **Unsloth Desktop**), `~/.unsloth/skills`, `~/.claude/skills`, `~/.codex/skills`, and `~/.gemini/antigravity-cli/skills`:

```bash
git clone https://github.com/Filenametxt/file-organizer.git ~/.local/share/agent-repos/file-organizer
~/.local/share/agent-repos/file-organizer/install.sh
```

### Option B: `npx skills` CLI

If you use the standard [Agent Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add Filenametxt/file-organizer
```

### Option C: Manual Symlink Installation

For **Unsloth Desktop (Unsloth Studio)** or any agent supporting `~/.agents/skills`:

```bash
mkdir -p ~/.agents/skills ~/.local/share/agent-repos
git clone https://github.com/Filenametxt/file-organizer.git ~/.local/share/agent-repos/file-organizer

ln -sfn ~/.local/share/agent-repos/file-organizer/skills/fsortcheck ~/.agents/skills/fsortcheck
ln -sfn ~/.local/share/agent-repos/file-organizer/skills/fsortdump  ~/.agents/skills/fsortdump
```

---

## Helper CLI Utility (`organizer_helper.py`)

Both skills bundle a zero-dependency Python helper script (`scripts/organizer_helper.py`) that agents or users can invoke on local or WebDAV-mounted directories:

```bash
# Audit a directory tree for Miller's Law (7 ± 2) compliance and README.md presence
python3 skills/fsortcheck/scripts/organizer_helper.py audit ~/Documents --depth 2

# Verify that a dump/inbox directory has 0 remaining items
python3 skills/fsortdump/scripts/organizer_helper.py verify-dump ~/Downloads
```

---

## Agent Compatibility Matrix

| AI Agent / IDE | Trigger Syntax | Status | Skill Directory |
|---|---|---|---|
| **Unsloth Desktop (Unsloth Studio)** | `@fsortcheck` / `@fsortdump` | **Tested & Verified** | `~/.agents/skills/` & `~/.unsloth/skills/` |
| **Claude Code** | `/fsortcheck` / `/fsortdump` | Compatible (`SKILL.md` + `.claude-plugin`) | `~/.claude/skills/` |
| **OpenAI Codex CLI** | `/fsortcheck` / `$fsortcheck` | Compatible (`SKILL.md` + `.codex-plugin`) | `~/.codex/skills/` |
| **Cursor** | `/fsortcheck` / `@fsortcheck` | Compatible (`SKILL.md` + `.cursor-plugin`) | `~/.cursor/skills/` or `.agents/skills/` |
| **Google Antigravity** | Mention `fsortcheck` / `fsortdump` | **Tested & Verified** | `~/.gemini/antigravity-cli/skills/` |
| **Windsurf / Cline / Roo Code / OpenCode** | `/fsortcheck` or mention | Compatible (`SKILL.md` standard) | `.agents/skills/` |

---

## Security Audit

Audited with **[NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector)** static & behavioral analyzers (AST, taint tracking, YARA, prompt injection, and exfiltration rules):

- **Risk Score**: Low (`SAFE`)
- **Dependencies**: Zero external Python dependencies (uses Python 3 standard library only)
- **Data Safety**: Fail-fast on HTTP/IO errors; zero destructive deletions without verification.

---

## Search Keywords & Topics

`agent-skills` · `ai-agents` · `file-organizer` · `millers-law` · `unsloth` · `unsloth-desktop` · `unsloth-studio` · `local-llm` · `llamacpp` · `mcp` · `model-context-protocol` · `nextcloud` · `claude-code` · `cursor` · `codex` · `antigravity` · `skill-md`

---

## License

Released under the [MIT License](LICENSE). Created by [@Filenametxt](https://github.com/Filenametxt).
