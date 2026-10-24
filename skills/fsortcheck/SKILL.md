---
name: fsortcheck
description: "Reorganize local filesystems or cloud storage (Nextcloud, WebDAV, Google Drive via MCP) applying Miller's Law (7 +- 2 items per folder), aligning with the user's mental model and generating self-documenting README.md files in each subfolder."
---

# fsortcheck — Filesystem Cognitive Restructuring (Miller's Law)

> **EXECUTION GATE**: If this `SKILL.md` is already loaded in your context, **DO NOT call `read_skill` again**. Immediately start Step 1 by calling your active storage/MCP tools.
> **EXACT TOOL NAMES**: Always call the **exact tool name** declared in your active tool definitions (for example, `mcp__...__nextcloud_list_files`, `mcp__...__nextcloud_move_file`, `mcp__...__nextcloud_create_folder`, `mcp__...__nextcloud_read_file`, `mcp__...__nextcloud_write_file`, or your local filesystem tools). **NEVER** invent bare function names that are not in your registered tool schema.

Reorganize any target directory or storage archive by applying **Miller's Law (7 ± 2 items per folder: optimal range 5 to 9)** across all directories, aligning with the user's category taxonomy (mental model), and generating a self-documenting `README.md` in every organized folder and subfolder.

---

## 1. Core Safety & Inspection Rules

1. **MOVE-ONLY POLICY (NEVER DELETE USER FILES)**:
   - You are a **File Organizer**, not a file deleter. Always **move** files to their organized folders; **never delete user files**.
   - **Single Exception (Identical Hash Duplicates)**: A duplicate file may only be deleted if you have verified that an identical copy already exists with the **exact same cryptographic hash (SHA-256 / MD5)** and byte size. If two files share a name but differ in content/hash, rename one (`_v2`) and move it.
   - **Never** delete a permanent inbox/dump container folder (`/Upload`, `/Downloads`, `/Inbox`).

2. **`size_bytes: 0` ON A DIRECTORY NEVER MEANS IT IS EMPTY**:
   - In Nextcloud, WebDAV, and MCP listings, every directory (`"is_directory": true`) **always reports `"size_bytes": 0`** even when full of files.
   - **Never** assume a directory is empty based on `size_bytes: 0`. Always call your list-files tool directly on that directory path to see its actual contents.

3. **MANDATORY RE-CHECK BEFORE REMOVING ANY CONSOLIDATED FOLDER SHELL**:
   - If you consolidate an old directory (e.g., `/Documents` or `/Notes`) into the user's categories and plan to remove the empty old directory shell, you **must** call your list-files tool on that directory in the immediately preceding step and confirm it returns `[]` (`0` items). If even 1 user item remains inside, move it first—never delete a non-empty folder.
   - **Never** move one folder's `README.md` into another folder (doing so would overwrite the destination folder's `README.md`).

4. **ATOMIC SOFTWARE PROJECT PROTECTION (Never Fragment Codebases)**:
   - If a folder is a **software or programming project** (contains `Cargo.toml`, `package.json`, `tsconfig.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `CMakeLists.txt`, `Makefile`, `pom.xml`, `build.gradle`, `pubspec.yaml`, `Dockerfile`, or `.git`), treat the **entire project directory as an indivisible atomic unit**.
   - **Never** split, rename, or move internal files/folders inside a code project (`src/`, `target/`, `Cargo.toml`, etc.) and **never** overwrite a project's own `README.md`. You may only move the whole project folder intact into a parent category (e.g., `Projects/Rust/<project_name>`) if the parent exceeds 9 projects.

5. **CONTENT INSPECTION & TOOL-CAPABILITY LEARNING**:
   - Read existing folder `README.md` files first as the primary source of truth.
   - Read file contents when a reader tool is available. If an extension (e.g., `.docx`, `.zip`, binary files, or images without vision tools) fails or returns binary bytes, **remember that extension as unreadable** for the session and skip reading subsequent files of that extension, inferring context from filename and path instead.

6. **SELF-DOCUMENTING `README.md` & LANGUAGE ADAPTATION**:
   - Communicate and write `README.md` files in the **same language used by the user**.
   - For every organized folder and newly created subfolder, create or update its `README.md` so future LLMs know what belongs inside.
   - Work **one folder at a time** and **stop immediately (Fail-Fast)** if any file move returns an error (such as HTTP 404).

---

## 2. Standard `README.md` Template for Folders

```markdown
# [Folder Name]

## Purpose & Context
[Brief description of what this folder represents and its semantic scope]

## Allowed Contents
- [Typical file types stored here]

## Routing Rules for LLMs
- **Route here**: [Semantic criteria for placing new files into this folder]
- **Subfolders**: [List and purpose of child subfolders, if any]
- **Cognitive Target**: Maintain 5 to 9 items (Miller's Law: 7 ± 2).
```

---

## 3. Step-by-Step Operational Workflow

1. **Step 1 — Root Scan & Category Alignment**:
   - Call your list-files tool (e.g., `mcp__...__nextcloud_list_files`) on the root directory `/` and on each non-excluded directory to count actual items.
   - If the user has not specified their top-level categories, propose categories (`Personal`, `University`, `Finance`, `Projects`) and ask for confirmation.
2. **Step 2 — Folder-by-Folder Reorganization (Miller's Law: 5 to 9 Items)**:
   - For each directory with **more than 9 items (OVERFLOW)** or needing consolidation into the user's categories:
     1. Inspect contents with your list-files tool (and check subfolders to protect atomic software projects).
     2. Create logical thematic subfolders using your create-folder tool (e.g., `mcp__...__nextcloud_create_folder`) so every folder holds **5 to 9 items**.
     3. Move files into their subfolders using your move-file tool (e.g., `mcp__...__nextcloud_move_file`). If a destination folder with the same name already exists, move inner items individually.
     4. Write or update the `README.md` in the parent folder and each new subfolder using your write-file tool (e.g., `mcp__...__nextcloud_write_file`).
     5. Re-check with your list-files tool to confirm item counts (`5–9`) and verify `[]` (`0` items) before removing any consolidated empty folder shell.
3. **Step 3 — Final Summary**:
   - Once all folders are balanced and documented, present a clean summary table of reorganized folders, moved files, and generated `README.md` indexes.
