---
name: fsortdump
description: "Empty and reorganize files and subfolders from a dump or inbox folder (Upload, Downloads, Inbox) into the structured filesystem by semantic context, guaranteeing zero remainder and updating subfolder README.md files."
---

# /fsortdump — Dump / Inbox Zero-Remainder Organizer

Completely empty the **contents** (both loose files and subfolders) of a transit, inbox, or dump directory (such as `Upload`, `Downloads`, or `Inbox`) by analyzing the semantic context of every file and subfolder, routing everything into the organized filesystem, and guaranteeing **zero remaining items inside the dump folder** while respecting **Miller's Law (7 ± 2)**.

---

## 1. Non-Negotiable Safety & Inspection Rules

1. **NEVER DELETE THE DUMP FOLDER ITSELF (`/Upload`, `/Downloads`, `/Inbox`)**:
   - **ABSOLUTE PROHIBITION**: **NEVER** call `delete_file` or `rmdir` on the root dump/inbox folder itself (e.g., **NEVER** delete `/Upload`).
   - "Leaving `Upload` completely empty" means moving all files and subfolders **out of** `Upload` so the `Upload` directory remains alive as an empty container (`list_files("/Upload")` returns `[]` or only `Upload/README.md`).
   - **NEVER move `Upload/README.md` into another folder** (e.g., never move `Upload/README.md` to `Personal/README.md`, as that overwrites the destination folder's index!).

2. **`size_bytes: 0` ON A FOLDER DOES NOT MEAN IT IS EMPTY!**:
   - In Nextcloud, WebDAV, and MCP directory listings, every directory (`"is_directory": true`) **ALWAYS reports `"size_bytes": 0`** even when it contains hundreds of files and subfolders!
   - **NEVER** assume a folder or subfolder is empty because `size_bytes` is `0`.
   - The **ONLY** valid proof that a folder is empty is calling `list_files(path="<folder_path>")` directly on that folder and receiving an empty list `[]` (`0` items).

3. **INSPECT EVERY SUBFOLDER INSIDE THE DUMP FOLDER (`Upload/<subfolder>`)**:
   - When you run `list_files("/Upload")`, you must account for **every single item returned** — both files (`"is_directory": false`) and directories (`"is_directory": true`). Never skip or overlook a directory (such as `Upload/Code`, `Upload/Tesi`, etc.).
   - For **every subfolder** (`"is_directory": true`) inside `Upload`, you **MUST call `list_files("Upload/<subfolder>")` first** to inspect its contents before moving or deleting anything:
     - **If it is a Software/Code Project** (contains `Cargo.toml`, `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `CMakeLists.txt`, `Makefile`, `pom.xml`, `build.gradle`, `Dockerfile`, or `.git/`): treat it as an **ATOMIC unit**. Never split its internal files; move the entire project folder intact to `Projects/<project_name>` (or `Progetti/<project_name>`).
     - **If the destination already has a folder with the same name** (e.g., `Upload/Tesi` when `Università/Tesi` already exists, or `Upload/Code` when `Progetti/Code` already exists): calling `move_file("Upload/Tesi", "Università/Tesi")` may fail or leave `Upload/Tesi` behind! Instead, call `list_files("Upload/<subfolder>")`, move the individual files/items inside `Upload/<subfolder>/...` to their destination, and then verify `list_files("Upload/<subfolder>")` is `[]` before removing the empty `Upload/<subfolder>`.

4. **MANDATORY RE-CHECK (`list_files`) BEFORE ANY FOLDER DELETION OR COMPLETION**:
   - **Before calling `delete_file` on ANY subfolder** (e.g., `Upload/<subfolder>`), you **MUST** call `list_files("Upload/<subfolder>")` in the step immediately prior and confirm it returns `[]` (`0` files and `0` folders). If even 1 item is inside, **DO NOT DELETE IT** — move the items inside first!
   - **After moving all items**, you **MUST** call `list_files("/Upload")` again to verify whether any files or subfolders are still inside `/Upload` (for example, if a directory move did not remove the source directory). You may only finish when `list_files("/Upload")` confirms `0` remaining user items.

5. **CONTENT INSPECTION & TOOL-CAPABILITY LEARNING**:
   - Before routing a file into a destination folder, read that folder's `README.md` if present.
   - Inspect file contents when a reader tool is available.
   - **Memory of Unsupported Formats**: If a file extension (e.g., `.docx`, `.zip`, binary files, or images without vision tools) fails to read or returns binary bytes, **remember that extension as unreadable** for the session and skip reading subsequent files of that same extension, routing them by filename and path context instead.

6. **LANGUAGE ADAPTATION & DIRECT TOOL EXECUTION**:
   - Communicate and write `README.md` files in the **same language used by the user**.
   - Emit **real tool calls immediately** (`list_files`, `create_folder`, `move_file`, `write_file`). Never write pseudo-code tool calls in thoughts or text.
   - **Strict Fail-Fast**: If a file move returns HTTP 404 or an I/O error, stop immediately and report the exact error without deleting anything.

---

## 2. Standard `README.md` Template for New Destination Folders

Whenever you create a new subfolder in the main filesystem (for instance, to respect **Miller's Law: 5 to 9 items per folder**), create a `README.md` inside it:

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

### Step 1: Full Inventory of Dump Folder & Root Categories
1. Call `list_files` on the root directory (to see the exact names of the main destination folders, e.g. `Personal`, `Università`, `Finanze`, `Progetti`).
2. Call `list_files` on the dump folder (e.g. `/Upload`).
3. List out **all** items found in `/Upload`, explicitly separating:
   - **Loose files** (`"is_directory": false`, ignoring `Upload/README.md` so you never move `Upload/README.md` over another folder's `README.md`).
   - **Subfolders** (`"is_directory": true`, e.g. `Upload/Code`, `Upload/Tesi`, `Upload/To save uni`).
4. For **every subfolder** found inside `/Upload`, immediately call `list_files("/Upload/<subfolder>")` (and recursively on any nested subfolders) so you know every single file and project inside them! Remember: `"size_bytes": 0` on a directory **never** means it is empty.

### Step 2: Route Loose Files & Subfolder Contents
1. **Route Loose Files**:
   - Move each file (`move_file`) to its matching destination folder according to semantic context and destination `README.md` rules.
2. **Route Subfolders (`Upload/<subfolder>`)**:
   - If `Upload/<subfolder>` is already empty (`list_files("/Upload/<subfolder>")` returned `[]`), you may delete the empty subfolder `Upload/<subfolder>`.
   - If `Upload/<subfolder>` is an **Atomic Software Project** (`Cargo.toml`, `package.json`, `.git`, etc.), move the entire project folder intact into the Projects category (e.g. `Progetti/<subfolder>`).
   - Otherwise, if a folder with that name or theme already exists in the destination (or if it is a collection of loose documents like `Upload/Tesi`, `Upload/To save uni`, `Upload/Code`), move each item inside `Upload/<subfolder>/...` to its appropriate destination category/subfolder.
   - If any destination folder exceeds **9 items** (Miller's Law: $7 \pm 2$), create a thematic subfolder with `create_folder` and write its `README.md`.

### Step 3: Mandatory Re-Check Before Deleting Subfolders or Finishing
1. For each subfolder `Upload/<subfolder>` that was emptied, call `list_files("/Upload/<subfolder>")` to **verify** it now returns `[]` (`0` items). Only after `list_files` confirms `[]` may you delete `/Upload/<subfolder>`.
2. Call `list_files("/Upload")` one final time to **verify** that the dump folder itself now contains `0` remaining files and `0` remaining subfolders (never delete `/Upload` itself!).
3. If `list_files("/Upload")` still shows any remaining file or subfolder, **do not delete it blindly** — inspect it with `list_files`, move its contents properly, and re-verify until `/Upload` is genuinely empty.
4. Present a clear summary table of all moved files and subfolders (`Source ➔ Destination`).
