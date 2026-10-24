#!/usr/bin/env python3
"""
File Organizer Helper Script
Cognitive load auditor based on Miller's Law (7 ± 2 rule: optimal range 5 to 9 items per folder)
and Zero-Remainder verifier for dump/inbox directories.
Backend-agnostic utility for local filesystems and mounted WebDAV/Nextcloud directories.
"""

import argparse
import os
import sys
from pathlib import Path

# Miller's Law: 7 ± 2 (optimal range: 5 to 9 items per directory)
IDEAL_MIN = 5
IDEAL_MAX = 9
TARGET_COUNT = 7


def audit_directory(root_path: Path, max_depth: int = 3, recursive: bool = True):
    """
    Scan directory structure and check compliance with Miller's Law (7 ± 2).
    """
    results = []
    root_path = root_path.resolve()

    if not root_path.exists():
        print(f"Error: Path '{root_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    for current_dir, dirs, files in os.walk(root_path):
        current = Path(current_dir)
        # Ignore hidden directories and files
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        visible_files = [f for f in files if not f.startswith(".") and f.lower() != "readme.md"]

        rel_path = current.relative_to(root_path)
        depth = len(rel_path.parts)
        if depth > max_depth:
            continue

        item_count = len(dirs) + len(visible_files)
        status = "OK"
        action = "Optimal (within Miller's Law: 5-9 items)"

        if item_count > IDEAL_MAX:
            status = "OVERFLOW"
            action = (
                f"Cognitive overload ({item_count} > {IDEAL_MAX}). "
                "Create thematic subfolders (by topic, year, or type)."
            )
        elif 0 < item_count < IDEAL_MIN and current != root_path:
            status = "SPARSE"
            action = f"Underpopulated ({item_count} < {IDEAL_MIN}). Consider consolidating."
        elif item_count == 0:
            status = "EMPTY"
            action = "Empty directory. Consider removing if unused."

        results.append(
            {
                "path": str(rel_path) if str(rel_path) != "." else "/",
                "folders": len(dirs),
                "files": len(visible_files),
                "total": item_count,
                "has_readme": any(f.lower() == "readme.md" for f in files),
                "status": status,
                "action": action,
            }
        )

        if not recursive:
            break

    return results


def check_dump_status(dump_path: Path):
    """
    Verify whether the dump/inbox directory is completely empty (zero-remainder).
    """
    dump_path = dump_path.resolve()
    if not dump_path.exists():
        return False, f"Dump directory '{dump_path}' does not exist."

    items = [item for item in dump_path.iterdir() if not item.name.startswith(".")]
    if len(items) == 0:
        return True, "Dump directory is completely empty (0 files, 0 folders)."
    else:
        file_list = ", ".join(item.name for item in items[:5])
        extra = f" (and {len(items) - 5} more)" if len(items) > 5 else ""
        return False, f"{len(items)} items remaining: {file_list}{extra}"


def main():
    parser = argparse.ArgumentParser(
        description="File Organizer Helper — Miller's Law (7 ± 2) Auditor & Dump Verifier"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: audit
    audit_parser = subparsers.add_parser(
        "audit", help="Audit cognitive load on a directory tree (Miller's Law: 7 ± 2)"
    )
    audit_parser.add_argument("path", type=str, help="Path to the directory to audit")
    audit_parser.add_argument(
        "--depth", type=int, default=3, help="Maximum scan depth (default: 3)"
    )
    audit_parser.add_argument(
        "--format", choices=["text", "markdown"], default="markdown", help="Output format"
    )

    # Subcommand: verify-dump
    dump_parser = subparsers.add_parser(
        "verify-dump", help="Verify that a dump/inbox folder has 0 remaining items"
    )
    dump_parser.add_argument("path", type=str, help="Path to the dump/inbox directory")

    args = parser.parse_args()

    if args.command == "audit":
        results = audit_directory(Path(args.path), max_depth=args.depth)
        if args.format == "markdown":
            print(f"### Cognitive Load Audit: `{args.path}` (Miller's Law: 7 ± 2)\n")
            print("| Folder | Subfolders | Files | Total | README.md | Status | Recommendation |")
            print("|---|---|---|---|---|---|---|")
            for r in results:
                readme_badge = "Yes" if r["has_readme"] else "No"
                print(
                    f"| `{r['path']}` | {r['folders']} | {r['files']} | {r['total']} "
                    f"| {readme_badge} | **{r['status']}** | {r['action']} |"
                )
        else:
            for r in results:
                readme_str = "[README]" if r["has_readme"] else "[NO-README]"
                print(
                    f"[{r['status']}] {r['path']} {readme_str} - {r['total']} items "
                    f"(Dirs:{r['folders']}, Files:{r['files']}) -> {r['action']}"
                )

    elif args.command == "verify-dump":
        is_empty, msg = check_dump_status(Path(args.path))
        if is_empty:
            print(f"SUCCESS: {msg}")
            sys.exit(0)
        else:
            print(f"WARNING: {msg}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
