---
name: fsortcheck
description: "Reorganize local filesystems or cloud storage (Nextcloud, WebDAV, Google Drive via MCP) applying Miller's Law (7 +- 2 items per folder), aligning with the user's mental model and generating self-documenting README.md files in each subfolder."
---

# /fsortcheck — Filesystem Cognitive Restructuring (Miller's Law)

Reorganize any target directory or storage archive by applying **Miller's Law (7 ± 2 items per folder: optimal range 5 to 9)** across all directories, aligning with the user's mental model (category taxonomy), and generating a self-documenting `README.md` in every organized folder and subfolder so future LLMs can understand the structure and make autonomous routing decisions.

---

## 1. Core Principles, Safety Verification & Tool-Capability Learning

1. **LANGUAGE ADAPTATION**:
   - Always communicate with the user and write generated `README.md` files in the **same language used by the user** (e.g., Italian if prompted in Italian, English if prompted in English).

2. **`size_bytes: 0` ON A DIRECTORY NEVER MEANS IT IS EMPTY!**:
   - In Nextcloud, WebDAV, and MCP directory listings, every directory (`"is_directory": true`) **ALWAYS reports `"size_bytes": 0`** even when it contains hundreds of files and subfolders!
   - **NEVER** assume a directory or subfolder is empty because `size_bytes` is `0`.
   - The **ONLY** valid way to check what is inside a directory (or verify if it is empty) is to call `list_files(path="<directory_path>")` directly on that directory and verify the returned list.

3. **MANDATORY RE-CHECK (`list_files`) BEFORE DELETING ANY FOLDER**:
   - **NEVER** delete a permanent inbox/dump container folder (such as `/Upload`, `/Downloads`, `/Inbox`).
   - If you are consolidating an old folder (e.g., `/Documents` or `/Notes`) into the user's new categories and plan to remove the old folder after moving its contents, you **MUST** call `list_files(path="<old_folder>")` in the step immediately before calling `delete_file`.
   - If `list_files` returns **even 1 file or 1 subfolder** (other than an obsolete `README.md`), **DO NOT DELETE THE FOLDER**! First inspect and move all remaining items, and re-run `list_files` until it confirms the folder is empty.
   - **NEVER move one folder's `README.md` into another folder** (e.g., never move `Documents/README.md` to `Personal/README.md`, as that overwrites `Personal`'s index!).

4. **TOTAL COVERAGE WITH ATOMIC SOFTWARE PROJECT PROTECTION**:
   - Every directory in the target scope (unless explicitly excluded by the user) must be inspected with `list_files` and reorganized if it exceeds **9 items**.
   - **CRITICAL EXCEPTION — DO NOT FRAGMENT SOFTWARE / CODE PROJECTS**:
     - If a folder is a **software or programming project** (detected by markers such as `Cargo.toml` for Rust, `package.json` / `tsconfig.json` for JS/TS, `pyproject.toml` / `requirements.txt` for Python, `go.mod` for Go, `CMakeLists.txt` / `Makefile` for C/C++, `pom.xml` / `build.gradle` for Java/Kotlin, `pubspec.yaml` for Flutter/Dart, `*.sln` / `*.csproj`, `Dockerfile`, or `.git/`):
     - **Treat the entire project directory as a single ATOMIC unit.**
     - **NEVER split, rename, or move files/folders inside a code project** (e.g., never touch `src/`, `target/`, `Cargo.toml`, `lib/`, `tests/`), as doing so would break builds, imports, and version control.
     - You may only move the **whole project root folder intact** into a parent category (e.g., `Projects/Rust/<project_name>` or `Progetti/Code/<project_name>`) if the parent folder exceeds 9 projects, and you must **never overwrite an existing project's `README.md`**.

5. **CONTENT INSPECTION & DYNAMIC TOOL-CAPABILITY LEARNING**:
   - To accurately determine semantic context, **inspect file contents** whenever a suitable tool is available (e.g., text/markdown readers, vision tools for images, document parsers).
   - **Memory of Unsupported File Formats**:
     - If a file has an extension for which no reading tool is available, or the tool fails / returns unreadable binary bytes (e.g., `.docx`, `.zip`, raw binaries, or images without a vision tool):
     - **Remember that file extension as unreadable** for the remainder of the current session.
     - For all subsequent files sharing that extension, **skip reading the file body** and infer semantic context from the filename, extension, and path metadata.
     - If a dedicated tool for that format is available (or added in the future, e.g., a `.docx` MCP tool), use it normally.

6. **SELF-DOCUMENTING `README.md` IN EVERY FOLDER & SUBFOLDER**:
   - For every folder or subfolder created or reorganized, create or update a `README.md` file inside it.
   - This file enables both humans and future LLMs to immediately understand the folder's purpose, allowed file types, and routing rules without scanning every file inside.
   - **Read Existing `README.md` First**: Whenever inspecting a folder that already contains a `README.md`, read it first as the primary source of truth for routing decisions.

7. **DIRECT TOOL EXECUTION (Zero Reasoning Loops)**:
   - **NEVER** write pseudo-code tool calls (`tool_name(...)`) inside your reasoning/thought block or plain text response.
   - Emit **actual tool calls immediately** (`list_files`, `create_folder`, `move_file`, `write_file` via MCP or local filesystem/bash tools).
   - Work **one folder at a time**: complete the reorganization of one folder before moving to the next.

---

## 2. Standard `README.md` Template for Folders

Every `README.md` created inside a folder or subfolder must follow this concise structure (translated into the user's language):

```markdown
# [Folder Name]

## Purpose & Context
[Brief description of what this folder represents and its semantic scope]

## Allowed Contents
- [Typical file types and formats stored here, e.g., PDF invoices, medical reports, contracts, images]

## Routing Rules for LLMs
- **Route here**: [Semantic criteria for placing new files into this folder]
- **Subfolders**: [List and purpose of any child subfolders]
- **Cognitive Target**: Maintain 5 to 9 items (Miller's Law: 7 ± 2).
```

---

## 3. Step-by-Step Operational Workflow

### Step 1: Root Scan & Target Environment Detection
- Identify the target backend specified by the user:
  - **MCP Server** (e.g., Nextcloud `nextcloud_list_files`, WebDAV, Google Drive, or generic `filesystem_list_directory`).
  - **Local Filesystem** (system tools or `python3 scripts/organizer_helper.py audit <path>`).
- Scan the root or target path and call `list_files` on each subdirectory to count its actual items (never rely on `size_bytes: 0`).
- If the user has not yet specified their **category classification (mental model)**, briefly propose top-level categories and ask for confirmation:
  - **Personal** (ID documents, contracts, health/medical)
  - **University / Study** (Exams, courses, thesis projects, papers)
  - **Finance** (Expenses, receipts, bank statements, taxes)
  - **Projects** (Software, scripts, repositories, reports)
  - Or other macro-areas matching the existing structure (e.g., `Photos`, `Archive`).

### Step 2: Folder-by-Folder Reorganization (Miller's Law: 7 ± 2)
For each folder containing **more than 9 items (OVERFLOW)** or needing consolidation into the user's categories:
1. **Context Analysis**:
   - Call `list_files` on the folder to see all files AND subfolders inside it.
   - If a `README.md` already exists, read it to learn the folder's rules.
   - Inspect files: read a snippet for supported formats, or use filename/extension for formats remembered as unreadable.
   - For any subfolder (`"is_directory": true`), call `list_files` on it first to check whether it is an **Atomic Software Project** (`Cargo.toml`, `package.json`, `.git`, etc.) or a regular document subfolder.
2. **Create Thematic Subfolders**:
   - Group items logically (e.g., in `Photos`: `Photos/Nature`, `Photos/Events`; in `Documents`: `Documents/Health`, `Documents/Identity`) so the parent folder and each subfolder stay within **5 to 9 items**.
   - Immediately invoke `create_folder(path=...)` (or `mkdir -p`).
3. **Move Files Safely (Fail-Fast Protocol)**:
   - Move files into their respective subfolders using `move_file(from=..., to=...)` (or `mv`).
   - If a destination subfolder with the same name already exists, move the inner items individually and verify with `list_files` that the source subfolder is empty before removing it.
   - **FAIL-FAST**: If any move returns an error (e.g., **HTTP 404**, *File not found*, *Permission denied*), **STOP IMMEDIATELY**. Do not delete anything, do not invent fallback files, and report the exact error to the user.
4. **Generate `README.md`**:
   - Write the `README.md` inside the reorganized parent folder and inside each newly created subfolder.
5. **Verify Count & Re-Check (`list_files`)**:
   - Call `list_files` on the folder to confirm that all moves succeeded and that item counts now respect the **5 to 9 items** range.
   - Never delete any obsolete folder without first calling `list_files` on it and proving it contains `0` remaining user items.

### Step 3: Proceed to Next Folder & Final Summary
- Repeat Step 2 for the next folder until the entire target tree is balanced and documented.
- Present a clean summary table showing created subfolders, generated `README.md` files, moved files, and final item counts.
