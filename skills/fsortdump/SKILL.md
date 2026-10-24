---
name: fsortdump
description: "Empty and reorganize files and subfolders from a dump or inbox folder (Upload, Downloads, Inbox) into the structured filesystem by semantic context, guaranteeing zero remainder and updating subfolder README.md files."
---

# /fsortdump — Dump / Inbox Zero-Remainder Organizer

Completely empty the **contents** (both loose files and subfolders) of a transit, inbox, or dump directory (such as `Upload`, `Downloads`, or `Inbox`) by analyzing the semantic context of every file and subfolder, **moving** everything into the organized filesystem, and guaranteeing **zero remaining items inside the dump folder** while respecting **Miller's Law (7 ± 2)**.

---

## 1. Non-Negotiable Safety, Move-Only & Inspection Rules

1. **ZERO FILE DELETION POLICY (MOVE-ONLY ORGANIZER)**:
   - **You are a File Organizer, NOT a File Deleter.** Your job is to **MOVE (`move_file`)** files and folders to their proper destination, **NEVER to delete user files (`delete_file` / `rm`)**.
   - **THE ONLY EXCEPTION FOR FILES — VERIFIED IDENTICAL DUPLICATES (SAME HASH)**:
     - You may delete a duplicate file **ONLY IF** you have verified that the exact same file already exists in the destination with the **identical cryptographic hash (SHA-256 / MD5)** (or verified byte-for-byte identical content and exact `size_bytes`).
     - **NEVER** assume two files are duplicates based only on having the same or similar filename! If two files have the same name but different hashes/sizes, rename the incoming file (e.g., `filename_v2.ext`) and **move** it so zero data is ever lost.
   - **EMPTY SUBFOLDER CLEANUP ONLY AFTER `list_files` = `[]`**:
     - You may only remove a leftover subfolder inside the dump directory (e.g., `Upload/<subfolder>`) **after** moving all of its contents out AND calling `list_files("Upload/<subfolder>")` in the immediately preceding step to prove it contains `[]` (`0` files and `0` folders).

2. **NEVER DELETE THE DUMP FOLDER ITSELF (`/Upload`, `/Downloads`, `/Inbox`)**:
   - **ABSOLUTE PROHIBITION**: **NEVER** call `delete_file` or `rmdir` on the root dump/inbox folder itself (e.g., **NEVER** delete `/Upload`).
   - "Leaving `Upload` completely empty" means **moving** all files and subfolders **out of** `Upload` so the `Upload` directory remains alive as an empty container (`list_files("/Upload")` returns `[]` or only `Upload/README.md`).
   - **NEVER move `Upload/README.md` into another folder** (e.g., never move `Upload/README.md` to `Personal/README.md`, as that overwrites the destination folder's index!).

3. **`size_bytes: 0` ON A FOLDER DOES NOT MEAN IT IS EMPTY!**:
   - In Nextcloud, WebDAV, and MCP directory listings, every directory (`"is_directory": true`) **ALWAYS reports `"size_bytes": 0`** even when it contains hundreds of files and subfolders!
   - **NEVER** assume a folder or subfolder is empty because `size_bytes` is `0`.
   - The **ONLY** valid proof that a folder is empty is calling `list_files(path="<folder_path>")` directly on that folder and receiving an empty list `[]` (`0` items).

4. **INSPECT EVERY SUBFOLDER INSIDE THE DUMP FOLDER (`Upload/<subfolder>`)**:
   - When you run `list_files("/Upload")`, you must account for **every single item returned** — both files (`"is_directory": false`) and directories (`"is_directory": true`). Never skip or overlook a directory (such as `Upload/Code`, `Upload/Tesi`, `Upload/To save uni`, etc.).
   - For **every subfolder** (`"is_directory": true`) inside `Upload`, you **MUST call `list_files("Upload/<subfolder>")` first** to inspect its contents before moving anything:
     - **If it is a Software/Code Project** (contains `Cargo.toml`, `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `CMakeLists.txt`, `Makefile`, `pom.xml`, `build.gradle`, `Dockerfile`, or `.git/`): treat it as an **ATOMIC unit**. Never split its internal files; move the entire project folder intact to `Projects/<project_name>` (or `Progetti/<project_name>`).
     - **If the destination already has a folder with the same name** (e.g., `Upload/Tesi` when `Università/Tesi` already exists, or `Upload/Code` when `Progetti/Code` already exists): calling `move_file("Upload/Tesi", "Università/Tesi")` may not merge them and will leave `Upload/Tesi` behind! Instead, call `list_files("Upload/<subfolder>")`, **move** the individual files/items inside `Upload/<subfolder>/...` to their destination, and then verify `list_files("Upload/<subfolder>")` is `[]` before removing the empty directory shell `Upload/<subfolder>`.

5. **MANDATORY RE-CHECK (`list_files`) AFTER MOVES & BEFORE COMPLETION**:
   - **After moving all items**, you **MUST** call `list_files("/Upload")` again to verify whether any files or subfolders are still inside `/Upload`.
   - If any subfolder is still in `/Upload`, **NEVER call `delete_file` on it blindly**: call `list_files("/Upload/<subfolder>")`, move every remaining file inside it to the proper destination category, and re-verify with `list_files("/Upload/<subfolder>")` that it is `[]` before removing the empty subfolder shell.

6. **CONTENT INSPECTION & TOOL-CAPABILITY LEARNING**:
   - Before routing a file into a destination folder, read that folder's `README.md` if present.
   - Inspect file contents when a reader tool is available.
   - **Memory of Unsupported Formats**: If a file extension (e.g., `.docx`, `.zip`, binary files, or images without vision tools) fails to read or returns binary bytes, **remember that extension as unreadable** for the session and skip reading subsequent files of that same extension, routing them by filename and path context instead.

7. **LANGUAGE ADAPTATION & DIRECT TOOL EXECUTION**:
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

### Step 2: Move Loose Files & Subfolder Contents (Move-Only, Never Delete Files)
1. **Move Loose Files**:
   - Move each file (`move_file`) to its matching destination folder according to semantic context and destination `README.md` rules.
   - If a file with the same name already exists in the destination, check whether they have the exact same cryptographic hash (or identical byte-for-byte content and size). Only if they are verified identical duplicates may the redundant copy be removed; otherwise rename and move (`filename_v2.ext`).
2. **Move Subfolders (`Upload/<subfolder>`)**:
   - If `Upload/<subfolder>` is an **Atomic Software Project** (`Cargo.toml`, `package.json`, `.git`, etc.), move the entire project folder intact into the Projects category (e.g. `Progetti/<subfolder>`).
   - Otherwise, move each item inside `Upload/<subfolder>/...` to its appropriate destination category/subfolder using `move_file`.
   - If any destination folder exceeds **9 items** (Miller's Law: $7 \pm 2$), create a thematic subfolder with `create_folder` and write its `README.md`.

### Step 3: Mandatory Re-Check (`list_files`) & Final Summary Report
1. For each subfolder `Upload/<subfolder>` whose contents were moved out, call `list_files("/Upload/<subfolder>")` to **verify** it now returns `[]` (`0` items). Only after `list_files` confirms `[]` may you remove the empty directory shell `/Upload/<subfolder>`.
2. Call `list_files("/Upload")` one final time to **verify** that the dump folder itself now contains `0` remaining files and `0` remaining subfolders (never delete `/Upload` itself!).
3. **MANDATORY FINAL SUMMARY REPORT**: Once `list_files("/Upload")` confirms the dump folder is empty, you **MUST** output a concise final summary report (translated into the user's language) following this exact structure:

```markdown
### Summary Report (`/fsortdump`)

**1. Moved Files & Subfolders (`Source ➔ Destination`)**
- `Upload/file.ext` ➔ `Category/Subfolder/file.ext`
- `Upload/Subfolder/item.ext` ➔ `Category/item.ext`
- `Upload/project_dir/` ➔ `Projects/project_dir/` *(Atomic Project)*

**2. New Subfolders & `README.md` Indexes Created**
- `Category/Subfolder/` (`README.md` generated)

**3. Dump Folder Verification (`list_files`)**
- `Upload/` verified empty (`0` remaining files, `0` remaining subfolders). Zero user files deleted.
```
