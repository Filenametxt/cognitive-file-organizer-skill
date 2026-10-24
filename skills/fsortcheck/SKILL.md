---
name: fsortcheck
description: "Reorganize local filesystems or cloud storage (Nextcloud, WebDAV, Google Drive via MCP) applying Miller's Law (7 +- 2 items per folder), aligning with the user's mental model and generating self-documenting README.md files in each subfolder."
---

# /fsortcheck — Filesystem Cognitive Restructuring (Miller's Law)

Reorganize any target directory or storage archive by applying **Miller's Law (7 ± 2 items per folder: optimal range 5 to 9)** across all directories, aligning with the user's mental model (category taxonomy), and generating a self-documenting `README.md` in every organized folder and subfolder so future LLMs can understand the structure and make autonomous routing decisions.

---

## 1. Core Principles, Inspection & Tool-Capability Learning

1. **LANGUAGE ADAPTATION**:
   - Always communicate with the user and write generated `README.md` files in the **same language used by the user** (e.g., Italian if prompted in Italian, English if prompted in English).

2. **TOTAL COVERAGE WITH ATOMIC SOFTWARE PROJECT PROTECTION**:
   - Every directory in the target scope (including `Photos`, `Templates`, `Documents`, `Upload`, `University`, `Projects`, etc.) must be inspected and reorganized if it exceeds **9 items**.
   - **CRITICAL EXCEPTION — DO NOT FRAGMENT SOFTWARE / CODE PROJECTS**:
     - If a folder is a **software or programming project** (detected by markers such as `Cargo.toml` for Rust, `package.json` / `tsconfig.json` for JS/TS, `pyproject.toml` / `requirements.txt` for Python, `go.mod` for Go, `CMakeLists.txt` / `Makefile` for C/C++, `pom.xml` / `build.gradle` for Java/Kotlin, `pubspec.yaml` for Flutter/Dart, `*.sln` / `*.csproj`, `Dockerfile`, or `.git/`):
     - **Treat the entire project directory as a single ATOMIC unit.**
     - **NEVER split, rename, or move files/folders inside a code project** (e.g., never touch `src/`, `target/`, `Cargo.toml`, `lib/`, `tests/`), as doing so would break builds, imports, and version control.
     - You may only move the **whole project root folder intact** into a parent category (e.g., `Projects/Rust/<project_name>` or `Projects/Python/<project_name>`) if the parent `Projects/` folder exceeds 9 projects, and you must **never overwrite an existing project's `README.md`**.

3. **CONTENT INSPECTION & DYNAMIC TOOL-CAPABILITY LEARNING**:
   - To accurately determine semantic context, **inspect file contents** whenever a suitable tool is available (e.g., text/markdown readers, vision tools for images, document parsers).
   - **Memory of Unsupported File Formats**:
     - If a file has an extension for which no reading tool is available, or the tool fails / returns unreadable binary bytes (e.g., `.docx`, `.zip`, raw binaries, or images without a vision tool):
     - **Remember that file extension as unreadable** for the remainder of the current session.
     - For all subsequent files sharing that extension, **skip reading the file body** and infer semantic context from the filename, extension, and path metadata.
     - If a dedicated tool for that format is available (or added in the future, e.g., a `.docx` MCP tool), use it normally.

4. **SELF-DOCUMENTING `README.md` IN EVERY FOLDER & SUBFOLDER**:
   - For every folder or subfolder created or reorganized, create or update a `README.md` file inside it.
   - This file enables both humans and future LLMs to immediately understand the folder's purpose, allowed file types, and routing rules without scanning every file inside.
   - **Read Existing `README.md` First**: Whenever inspecting a folder that already contains a `README.md`, read it first as the primary source of truth for routing decisions.

5. **DIRECT TOOL EXECUTION (Zero Reasoning Loops)**:
   - **NEVER** write pseudo-code tool calls (`tool_name(...)`) inside your reasoning/thought block or plain text response.
   - Emit **actual tool calls immediately** (`create_folder`, `move_file`, `write_file` via MCP or local filesystem/bash tools).
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
- Scan the root or target path and count items per directory.
- If the user has not yet specified their **category classification (mental model)**, briefly propose top-level categories and ask for confirmation:
  - **Personal** (ID documents, contracts, health/medical)
  - **University / Study** (Exams, courses, thesis projects, papers)
  - **Finance** (Expenses, receipts, bank statements, taxes)
  - **Projects** (Software, scripts, repositories, reports)
  - Or other macro-areas matching the existing structure (e.g., `Photos`, `Archive`).

### Step 2: Folder-by-Folder Reorganization (Miller's Law: 7 ± 2)
For each folder containing **more than 9 items (OVERFLOW)**:
1. **Context Analysis**:
   - If a `README.md` already exists, read it to learn the folder's rules.
   - Otherwise, inspect the files: read a snippet for supported formats, or use filename/extension for formats remembered as unreadable.
2. **Create Thematic Subfolders**:
   - Group items logically (e.g., in `Photos`: `Photos/Nature`, `Photos/Events`; in `Documents`: `Documents/Health`, `Documents/Identity`) so the parent folder and each subfolder stay within **5 to 9 items**.
   - Immediately invoke `create_folder(path=...)` (or `mkdir -p`).
3. **Move Files Safely (Fail-Fast Protocol)**:
   - Move files into their respective subfolders using `move_file(from=..., to=...)` (or `mv`).
   - **FAIL-FAST**: If any move returns an error (e.g., **HTTP 404**, *File not found*, *Permission denied*), **STOP IMMEDIATELY**. Do not delete anything, do not invent fallback files, and report the exact error to the user.
4. **Generate `README.md`**:
   - Write the `README.md` inside the reorganized parent folder and inside each newly created subfolder.
5. **Verify Count**:
   - Confirm that the folder and its subfolders now respect the **5 to 9 items** range.

### Step 3: Proceed to Next Folder & Final Summary
- Repeat Step 2 for the next overflowing folder until the entire target tree is balanced and documented.
- Present a clean summary table showing created subfolders, generated `README.md` files, moved files, and final item counts.
