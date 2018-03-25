import glob
import argparse

parser = argparse.ArgumentParser(description="AOT2 .ktsl2stbin files archiving tool.")
parser.add_argument("folder", help="folder with .kvs files")
args = parser.parse_args()
kfolder = args.folder

def read_bytes(filename):
    print("Reading file " + filename)
    b_list = []
    
    f = open(filename, 'rb')
    while True:
        piece = f.read(1024)  
        if not piece:
            break
        b_list.append(piece)
    f.close()

    return b_list
    
def write_file(name):
    print("Writing file "+name)
    # First 96 bytes (0x60)
    # This probably only works with AOT2 because the header might be different in each game
    header = b'KTSR\x02\x94\xdd\xfc\x01\x00\x00\x016\x0e\xf4\x05\x00\x00\x00\x00\x00\x00\x00\x00\x10\xf7\x05&\x10\xf7\x05&\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\xd4\xf4\x15 \xe9\x88\x00\xca\xab\xa8\xa9 \x00\x00\x00\xf7\xe8\x88\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    new_file = open(name, "wb")
    new_file.write(header + b"".join(fbytes))
    new_file.close()

files = glob.glob(kfolder+'/*.[kK][vV][sS]')
fbytes = []

for f in files:
    fbytes.append(b"".join(read_bytes(f)))
    
write_file("mod.ktsl2stbin")