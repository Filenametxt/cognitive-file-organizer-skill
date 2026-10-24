---
name: fsortdump
description: "Empty and reorganize files from a dump or inbox folder (Upload, Downloads, Inbox) into the structured filesystem by semantic context, guaranteeing zero remainder and updating subfolder README.md files."
---

# /fsortdump — Dump / Inbox Zero-Remainder Organizer

Completely empty a transit, inbox, or dump directory (such as `Upload`, `Downloads`, or `Inbox`) by analyzing the semantic context of every file and folder (reading contents where supported and consulting destination `README.md` files), routing everything into the organized filesystem, and guaranteeing **zero remaining items** while respecting **Miller's Law (7 ± 2)**.

---

## 1. Core Principles, Documentation & Tool-Capability Learning

1. **LANGUAGE ADAPTATION**:
   - Always communicate with the user and write generated `README.md` files in the **same language used by the user** (e.g., Italian if prompted in Italian, English if prompted in English).

2. **CONTENT INSPECTION & DESTINATION `README.md` LOOKUP**:
   - Before routing a file into a candidate destination folder, if that folder contains a `README.md`, **read it first**: it is the primary source of truth on whether the file belongs there.
   - To understand the semantic context of a file in the dump folder, **read its content** when a suitable tool is available.
   - **Memory of Unsupported File Formats (Tool-Capability Learning)**:
     - If a file extension (e.g., `.docx`, `.zip`, raw binaries, or images without a vision tool) lacks a reading tool or returns an error / binary bytes:
     - **Remember that extension as unreadable** for the current session.
     - For all subsequent files with the same extension, **skip reading the file body** and infer the destination from the filename, extension, and folder context.
     - If a dedicated tool for that format is present in the environment, use it normally.

3. **GENERATE `README.md` IN NEW DESTINATION FOLDERS**:
   - Whenever you create a new folder or subfolder in the main filesystem to receive items from the dump:
     - Generate a `README.md` inside it describing its purpose, allowed file types, and routing rules for future LLMs.

4. **DIRECT TOOL EXECUTION (Zero Reasoning Loops)**:
   - Never simulate or write pseudo-code tool calls (`tool_name(...)`) inside your thought block or text response.
   - Emit **actual tool calls immediately** (`create_folder`, `move_file`, `write_file`).

5. **STRICT FAIL-FAST ON ERRORS**:
   - If any file operation returns an error (e.g., **HTTP 404**, *File not found*, *Permission denied*):
     1. **STOP IMMEDIATELY**. Do not proceed with subsequent files.
     2. Do not delete anything from the dump folder.
     3. Report the exact filename and error to the user.

6. **ZERO-REMAINDER GUARANTEE**:
   - At the end of the process, explicitly run `list_files` on the dump directory to verify and certify that it contains **0 files and 0 folders**.

---

## 2. Standard `README.md` Template for Folders

```markdown
# [Folder Name]

## Purpose & Context
[Brief description of what this folder represents and its semantic scope]

## Allowed Contents
- [Typical file types and formats stored here, e.g., PDF receipts, reports, images, code]

## Routing Rules for LLMs
- **Route here**: [Semantic criteria for placing new files into this folder]
- **Cognitive Target**: Maintain 5 to 9 items (Miller's Law: 7 ± 2).
```

---

## 3. Step-by-Step Operational Workflow

### Step 1: Initial Scan of the Dump Folder & Root Taxonomy
- Identify the target backend (MCP server such as Nextcloud/WebDAV/Filesystem, or local filesystem tools) and the dump folder path (default: `Upload`, or user-specified such as `Downloads` / `Inbox`).
- Run `list_files` on both the root filesystem (to see existing destination categories) and the dump folder.
- If the dump folder is already empty, inform the user and stop.

### Step 2: Semantic Context Analysis & Routing
For each item inside the dump folder:
- **Pre-structured subfolders** (e.g., a folder containing personal IDs, or a course project folder): inspect its contents and move it directly into the matching macro-category (`Documents/`, `Personal/`, `University/`, `Projects/`, `Finance/`, `Archive/`).
- **Individual files**:
  - Read content if supported, or infer from filename/extension if the format is remembered as unreadable.
  - Check existing destination `README.md` files to confirm the best match.
  - If creating a new subfolder (or if a destination folder exceeds **9 items** under Miller's Law), create the thematic subfolder with `create_folder` and write its `README.md`.
  - Move the item using `move_file(from, to)`.

### Step 3: Fail-Fast Verification
- Verify each move succeeded. If any server or I/O error occurs (such as HTTP 404), halt immediately and report to the user.

### Step 4: Final "Zero-Remainder" Audit & Summary Report
- Call `list_files` on the dump folder (or run `python3 scripts/organizer_helper.py verify-dump <dump_path>` for local directories).
- Confirm that the dump folder has **0 remaining files and 0 remaining folders**.
- Present a clear markdown table of all moved items (`Source ➔ Destination`) and any created/updated `README.md` files.
