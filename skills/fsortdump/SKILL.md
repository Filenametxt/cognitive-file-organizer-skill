---
name: fsortdump
description: "Empty and reorganize files and subfolders from a dump or inbox folder (Upload, Downloads, Inbox) into the structured filesystem by semantic context, guaranteeing zero remainder and updating subfolder README.md files."
---

# fsortdump — Dump / Inbox Zero-Remainder Organizer

> **EXECUTION GATE**: If this `SKILL.md` is already loaded in your context, **DO NOT call `read_skill` again**. Immediately start Step 1 by calling your active storage/MCP tools.
> **EXACT TOOL NAMES**: Always call the **exact tool name** declared in your active tool definitions (for example, `mcp__...__nextcloud_list_files`, `mcp__...__nextcloud_move_file`, `mcp__...__nextcloud_create_folder`, `mcp__...__nextcloud_read_file`, `mcp__...__nextcloud_write_file`, or your local filesystem tools). **NEVER** invent bare function names that are not in your registered tool schema.

Completely empty the **contents** (both loose files and subfolders) of a transit, inbox, or dump directory (such as `Upload`, `Downloads`, or `Inbox`) by moving every file and subfolder into the organized filesystem, respecting **Miller's Law (7 ± 2: 5 to 9 items per folder)** and updating subfolder `README.md` indexes.

---

## 1. Core Safety & Inspection Rules

1. **MOVE-ONLY POLICY (NEVER DELETE USER FILES)**:
   - You are a **File Organizer**, not a file deleter. Always **move** files to their destination; **never delete user files**.
   - **Single Exception (Identical Hash Duplicates)**: A duplicate file may only be deleted if you have verified that an identical copy already exists at the destination with the **exact same cryptographic hash (SHA-256 / MD5)** and byte size. If two files share a name but differ in content/hash, rename the incoming file (`_v2`) and move it.

2. **NEVER DELETE THE ROOT DUMP FOLDER ITSELF (`/Upload`, `/Downloads`, `/Inbox`)**:
   - **Never** delete the `/Upload` container directory itself. "Leaving `Upload` empty" means moving all files and subfolders **out of** `Upload` so `Upload` remains as an empty container ready for future uploads.
   - **Never** move `Upload/README.md` into another folder (doing so would overwrite the destination folder's `README.md`).

3. **`size_bytes: 0` ON A DIRECTORY NEVER MEANS IT IS EMPTY**:
   - In Nextcloud, WebDAV, and MCP listings, every directory (`"is_directory": true`) **always reports `"size_bytes": 0`** even when full of files.
   - **Never** assume a directory is empty based on `size_bytes: 0`. You must call your list-files tool directly on that directory path and confirm the returned list is `[]` (`0` items).

4. **INSPECT EVERY SUBFOLDER INSIDE THE DUMP FOLDER (`Upload/<subfolder>`)**:
   - Account for **every** file (`"is_directory": false`) and **every** directory (`"is_directory": true`) in `Upload`.
   - For **every subfolder** inside `Upload` (e.g., `Upload/Code`, `Upload/Tesi`, `Upload/To save uni`), call your list-files tool on `Upload/<subfolder>` **before** acting:
     - **Atomic Software Projects**: If the subfolder contains code project markers (`Cargo.toml`, `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `CMakeLists.txt`, `Makefile`, `pom.xml`, `build.gradle`, `Dockerfile`, `.git`), treat the whole project folder as an **indivisible atomic unit** and move the entire project folder intact into the Projects category. Never split its internal files.
     - **Existing Destination Folder / Regular Subfolder**: If a folder with the same name already exists in the destination (e.g., `Università/Tesi` or `Progetti/Code`), moving the whole directory may leave the source behind. Instead, list the files inside `Upload/<subfolder>` and **move** each inner file/project to its destination category.

5. **MANDATORY RE-CHECK BEFORE REMOVING EMPTY SUBFOLDER SHELLS**:
   - Before removing any emptied subfolder shell `Upload/<subfolder>`, you **must** call your list-files tool on `Upload/<subfolder>` in the immediately preceding step and verify it returns `[]` (`0` items). If even 1 item remains inside, move it first—never delete a non-empty folder.
   - Before finishing, call your list-files tool on `/Upload` one final time to confirm `0` remaining user files and `0` remaining subfolders.

6. **CONTENT INSPECTION & TOOL-CAPABILITY LEARNING**:
   - Read existing destination `README.md` files first to confirm where files belong.
   - Read file contents when a reader tool is available. If an extension (e.g., `.docx`, `.zip`, binary files, or images without vision tools) fails or returns binary bytes, **remember that extension as unreadable** for the session and skip reading subsequent files of that extension, routing them by filename and path context.

7. **LANGUAGE ADAPTATION & FAIL-FAST**:
   - Communicate and write `README.md` files in the **same language used by the user**.
   - If any file move fails with an error (such as HTTP 404), **stop immediately** and report the error.

---

## 2. Standard `README.md` Template for New Subfolders

Whenever you create a new subfolder in the main filesystem (for instance, when a destination folder exceeds **9 items** under Miller's Law $7 \pm 2$), write a `README.md` inside it:

```markdown
# [Folder Name]

## Purpose & Context
[Brief description of what this folder represents and its semantic scope]

## Allowed Contents
- [Typical file types stored here]

## Routing Rules for LLMs
- **Route here**: [Semantic criteria for placing new files into this folder]
- **Cognitive Target**: Maintain 5 to 9 items (Miller's Law: 7 ± 2).
```

---

## 3. Step-by-Step Operational Workflow

1. **Step 1 — List Root & Dump Folder**:
   - Call your list-files tool (e.g., `mcp__...__nextcloud_list_files`) on the root directory `/` (to see exact category folder names, e.g., `Personal`, `Università`, `Finanze`, `Progetti`) and on `/Upload`.
   - For **every subfolder** (`"is_directory": true`) found inside `/Upload`, call your list-files tool on `/Upload/<subfolder>` to see all files and projects inside it.
2. **Step 2 — Move Loose Files & Subfolder Contents**:
   - Move each loose file in `/Upload` (except `Upload/README.md`) to its matching destination category/subfolder using your move-file tool (e.g., `mcp__...__nextcloud_move_file`).
   - Move atomic software projects intact to `Projects/` (`Progetti/`), and move the contents of regular subfolders inside `/Upload/<subfolder>` to their proper destination folders.
   - If any destination folder exceeds **9 items**, create a thematic subfolder and write its `README.md`.
3. **Step 3 — Re-Verify & Report**:
   - Re-check each emptied `Upload/<subfolder>` with your list-files tool; only after confirming `[]` (`0` items), remove the empty subfolder shell.
   - Re-check `/Upload` with your list-files tool to confirm `0` remaining user items (never delete `/Upload` itself), then present a clear summary table (`Source ➔ Destination`).
