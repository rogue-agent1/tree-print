import os, argparse

def tree(path, prefix="", depth=-1, dirs_only=False, level=0):
    if depth >= 0 and level > depth: return []
    entries = sorted(os.listdir(path))
    if dirs_only: entries = [e for e in entries if os.path.isdir(os.path.join(path, e))]
    entries = [e for e in entries if not e.startswith(".")]
    lines = []
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        full = os.path.join(path, entry)
        lines.append(prefix + connector + entry)
        if os.path.isdir(full):
            ext = "    " if is_last else "│   "
            lines.extend(tree(full, prefix + ext, depth, dirs_only, level + 1))
    return lines

def main():
    p = argparse.ArgumentParser(description="Directory tree printer")
    p.add_argument("path", nargs="?", default=".")
    p.add_argument("-d", "--depth", type=int, default=-1)
    p.add_argument("--dirs-only", action="store_true")
    args = p.parse_args()
    print(os.path.basename(os.path.abspath(args.path)) or args.path)
    for line in tree(args.path, depth=args.depth, dirs_only=args.dirs_only):
        print(line)

if __name__ == "__main__":
    main()
