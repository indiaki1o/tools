#!/usr/bin/env python
# coding: utf-8

#%%
import os
import numpy as np
import argparse
import shutil
from tqdm import tqdm
# from progressbar import progressbar 
#%%
parser = argparse.ArgumentParser()
parser.add_argument("src_path", help="a source directory path.")
parser.add_argument("dst_path", help="a distination directory.")
parser.add_argument("size",     help="a number of sampling from files.")
#%%
args        = parser.parse_args()
src_path    = args.src_path
dst_path    = args.dst_path
ssize       = int(args.size)
# src_path =  os.getcwd()
#%%
def parse_dir_file_surface(path):
    tokens = os.listdir(path=path)
    isfile = [os.path.isfile(os.path.join(".", t)) for t in tokens]
    isdir = [os.path.isdir(os.path.join(".", t)) for t in tokens]
    file_path = [t for t,b in zip(tokens,isfile) if b]
    dir_path = [t for t,b in zip(tokens,isdir) if b]
    #
    ret = {}
    ret["file_path"] = file_path
    ret["dir_path"] = dir_path
    ret["tokens"] = tokens 
    ret["isfile"] = isfile
    ret["isdir"] = isdir
    return ret

#%%
def parse_files_deeply(path_list):
    fpath_list = []
    dirpath=[path_list]
    sep = os.sep
    
    while dirpath:
        # put separator to suffix
        currpath = dirpath.pop()
        dirname = os.path.dirname(currpath)
        if dirname:
            currpath = os.path.dirname(currpath) +sep +os.path.basename(currpath) + sep
        else:
            currpath = os.path.basename(currpath) + sep
            
#         print("currpath", currpath)
        filedir = parse_dir_file_surface(currpath)
        fpath_list   = fpath_list + [currpath+p for p in filedir["file_path"]]
        dirpath = dirpath + [currpath+p for p in filedir["dir_path"]]
#         print(dirpath)
    return fpath_list
#%%
fpath_list = parse_files_deeply(src_path)
path_sampled = np.random.choice(fpath_list, replace=False, size=ssize)
# %%
os.makedirs(dst_path, exist_ok=True)
for src in tqdm(path_sampled):
    print("src: {}, dst: {}".format(src, dst_path))
    shutil.copy(src, dst_path)
# %%
