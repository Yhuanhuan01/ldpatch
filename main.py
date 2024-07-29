import sys
import ld_patch



def help():
    print("[-] Usage: python main.py <libcname> <elfname>")
    exit(0)
    
def check():
    if len(sys.argv) < 2 or not sys.argv[1]:
        print("Not Found libc")
        help()
    if len(sys.argv) < 3 or not sys.argv[2]:
        print("Not Found elf")
        help()


if __name__ == '__main__':
    check()
    libc = sys.argv[1]
    elf = sys.argv[2]
    match_libc = ld_patch.Found(libc,elf)
    ld_patch.download(match_libc)
    ld_patch.patchelf(elf)
