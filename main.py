'''
test
'''
import sys
import ld_patch

libc = sys.argv[1]
elf = sys.argv[2]

if not sys.argv[1]:
    print("Not Found libc")
    exit(0)

if not sys.argv[2]:
    print("Not Found elf")
    exit(0)


if __name__ == '__main__':
    match_libc = ld_patch.Found(libc,elf)
    ld_patch.download(match_libc)
    ld_patch.patchelf(elf)