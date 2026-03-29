#!/usr/bin/env python3
"""tree_print - Directory tree visualization."""
import sys, argparse, json, os

def tree(path, prefix="", depth=0, max_depth=3, show_hidden=False, dirs_only=False):
    if depth > max_depth: return []
    lines = []
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return [f"{prefix}[Permission Denied]"]
    if not show_hidden:
        entries = [e for e in entries if not e.startswith(".")]
    if dirs_only:
        entries = [e for e in entries if os.path.isdir(os.path.join(path, e))]
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        full = os.path.join(path, entry)
        if os.path.isdir(full):
            lines.append(f"{prefix}{connector}{entry}/")
            ext = "    " if is_last else "│   "
            lines.extend(tree(full, prefix + ext, depth + 1, max_depth, show_hidden, dirs_only))
        else:
            size = os.path.getsize(full)
            lines.append(f"{prefix}{connector}{entry} ({size}B)")
    return lines

def main():
    p = argparse.ArgumentParser(description="Directory tree")
    p.add_argument("path", nargs="?", default=".")
    p.add_argument("-d", "--depth", type=int, default=3)
    p.add_argument("-a", "--all", action="store_true")
    p.add_argument("--dirs-only", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    lines = tree(args.path, max_depth=args.depth, show_hidden=args.all, dirs_only=args.dirs_only)
    if args.json:
        print(json.dumps({"root": args.path, "lines": len(lines), "tree": lines}))
    else:
        print(os.path.basename(os.path.abspath(args.path)) + "/")
        print("
".join(lines))

if __name__ == "__main__": main()
