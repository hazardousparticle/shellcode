#! /bin/bash

#check args
if [ $# == 0 ]; then
    echo "Usage: $0 [--32] asm_file"
    echo ""
    echo "--32   compile for i386"
    exit 1
fi

# generate shellcode
if [ $1 == "--32" ]; then
    nasm -f elf $2 -o /tmp/shellcode.o
    ld -m elf_i386 -o /tmp/shellcode /tmp/shellcode.o
else
    nasm -felf64 $1 -o /tmp/shellcode.o
    ld -o /tmp/shellcode /tmp/shellcode.o
fi


objdump -d /tmp/shellcode -M intel > /tmp/shellcode.txt

"$(dirname $0)"/generate_shellcode.py /tmp/shellcode.txt
