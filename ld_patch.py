import re
import subprocess
import time

def Found(libc,elf):# found libc's version
    global ld_flags
    command = "strings {} | grep GNU".format(libc)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output_libc = result.stdout
    command = "file {}".format(elf)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output_elf = result.stdout

    pattern = r'\(([^)]+)\)'
    match_libc = re.search(pattern, output_libc)
    if match_libc:
        print("[*] "+match_libc.group(1))
    else:
        print("[+] Not match libc version")
    
    pattern = r"64-bit"
    if re.search(pattern, output_elf):
        Get_libc_version = match_libc.group(1)[13:]+'_amd64'
        ld_flags = 'x64'
    else:
        Get_libc_version = match_libc.group(1)[13:]+'_i386' 
        ld_flags = 'x86'

    return Get_libc_version# get libc's version

def download(match_libc):
    global pwd
    download_flags = 0 # download's flag
    libc_version = match_libc
    command1 = "cat ~/glibc-all-in-one/list"
    result1 = subprocess.run(command1, shell=True, capture_output=True, text=True)
    output1 = result1.stdout
    command2 = "cat ~/glibc-all-in-one/old_list"
    result2 = subprocess.run(command2, shell=True, capture_output=True, text=True)
    output2 = result2.stdout

    lines_new = output1.splitlines()
    lines_old = output2.splitlines()
    print(libc_version)
    if libc_version in lines_new: # Check if the list contains libc version and change download's flag
        print(f"[*] {libc_version} 存在于list中")
        download_flags = 1
    elif(libc_version in lines_old):
        print(f"[*] {libc_version} 存在于old_list中")
        download_flags = 2
    else:
        print("[+] List Not have the libc version")
        print('[-] Check the list and choose the libc version you think is appropriate')
        print(lines_new + lines_old)
        time.sleep(1)
        print("[-] Please enter the libc version you want to patchelf")
        libc_version = input(">>>\n")
        if libc_version in lines_new: # Check if the list contains libc version and change download's flag
            print(f"[*]You enter {libc_version} 存在于list中")
            download_flags = 1
        elif(libc_version in lines_old):
            print(f"[*]You enter {libc_version} 存在于old_list中")
            download_flags = 2

    
    if download_flags != 0:
        if download_flags == 1:
                command3 = "sudo ~/glibc-all-in-one/download {}".format(libc_version)
                subprocess.run(command3, shell=True, capture_output=True, text=True)
                pwd = "~/glibc-all-in-one/libs/{}".format(libc_version)
                print(pwd)
        elif download_flags == 2:
                command3 = "sudo ~/glibc-all-in-one/download_old {}".format(libc_version)
                subprocess.run(command3, shell=True, capture_output=True, text=True)
                pwd = "~/glibc-all-in-one/libs/{}".format(libc_version)



def patchelf(elf):
    if ld_flags == 'x64':
        command = "chmod 777 {}".format(elf)
        subprocess.run(command, shell=True, capture_output=True, text=True)
        command = "patchelf --set-interpreter {}/ld-linux-x86-64.so.2 ./{}".format(pwd,elf)
        subprocess.run(command, shell=True, capture_output=True, text=True)
        command = "patchelf --set-rpath {} ./{}".format(pwd,elf)
        subprocess.run(command, shell=True, capture_output=True, text=True)
        print("[*] Success x64")
    elif ld_flags == 'x86':
        command = "chmod 777 {}".format(elf)
        subprocess.run(command, shell=True, capture_output=True, text=True)
        command = "patchelf --set-interpreter {}/ld-linux.so.2 ./{}".format(pwd,elf)
        subprocess.run(command, shell=True, capture_output=True, text=True)
        command = "patchelf --set-rpath {} ./{}".format(pwd,elf)
        subprocess.run(command, shell=True, capture_output=True, text=True)
        print("[*] Success x86")
    else:
         print("Fail patchelf")