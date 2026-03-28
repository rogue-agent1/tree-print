#!/usr/bin/env python3
"""tree_print - Display directory tree like the tree command."""
import sys,os
def tree(path,prefix="",max_depth=None,depth=0,show_hidden=False,dirs_only=False):
    if max_depth is not None and depth>max_depth:return 0,0
    entries=sorted(os.listdir(path))
    if not show_hidden:entries=[e for e in entries if not e.startswith(".")]
    if dirs_only:entries=[e for e in entries if os.path.isdir(os.path.join(path,e))]
    files=dirs=0
    for i,entry in enumerate(entries):
        fp=os.path.join(path,entry);is_last=i==len(entries)-1
        connector="└── " if is_last else "├── "
        if os.path.isdir(fp):
            print(f"{prefix}{connector}{entry}/");dirs+=1
            ext="    " if is_last else "│   "
            d,f=tree(fp,prefix+ext,max_depth,depth+1,show_hidden,dirs_only);dirs+=d;files+=f
        else:print(f"{prefix}{connector}{entry}");files+=1
    return dirs,files
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("path",nargs="?",default=".")
    p.add_argument("-d","--depth",type=int);p.add_argument("-a","--all",action="store_true")
    p.add_argument("--dirs",action="store_true");a=p.parse_args()
    print(a.path);d,f=tree(a.path,max_depth=a.depth,show_hidden=a.all,dirs_only=a.dirs)
    print(f"\n{d} directories, {f} files")
