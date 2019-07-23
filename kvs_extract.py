#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import mmap

parser = argparse.ArgumentParser(description=".ktsl2stbin files extraction tool.")
parser.add_argument("file", help=".ktsl2stbin file")
args = parser.parse_args()
kfile = args.file

def read_bytes(filename):
    print("Reading file...")
    b_list = []
    
    f = open(filename, 'rb')
    while True:
        piece = f.read(1024)  
        if not piece:
            break
        b_list.append(piece)
    f.close()

    return b_list
    
def write_file(name, start, end):
    print("Writing file "+name)
    new_file = open(name, "wb")
    new_file.write(byte_str[start:end])
    new_file.close()
    
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

byte_str = b"".join(read_bytes(kfile))

ext = ".kvs"
files_start = list(find_all(byte_str, b'KOVS'))

if not files_start:
    files_start = list(find_all(byte_str, b'KTSS'))
    ext = ".kns"

last_offset = os.path.getsize(kfile)-1

out = os.path.join(os.path.dirname(kfile), os.path.basename(kfile).split(".")[0])
os.makedirs(out, exist_ok=True)

size = len(files_start)
print(size, "files")

for i in range(size-1):
    write_file(os.path.join(out, (str(i) if i>=10 else "0"+str(i))+ext), files_start[i], files_start[i+1])
else:
    write_file(os.path.join(out, str(size-1)+ext), files_start[-1], last_offset)
