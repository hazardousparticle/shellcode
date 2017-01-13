#! /bin/env python3

# generate ASM instructions that add a string to the stack

import sys
toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])

def make_chunks(msg,length):
    return (msg[i:length+i] for i in range(0,len(msg), length))

if __name__ == "__main__":
    bits = 64
    register = "rbx"
    
    if len(sys.argv) == 1:
        print("Usage: " + str(sys.argv[0]) + " string [--32]")
        exit(1)

    if len(sys.argv) > 2:
        if str(sys.argv[2]) == "--32":
            # 32 bit mode
            bits = 32
            register = "ebx"
            

    msg = str(sys.argv[1])
    
    chunks = list(make_chunks(msg, int(bits/8)))
    
    encoded_string = []
    for chunk in chunks:
        new_chunk = chunk[::-1]
        new_chunk = toHex(new_chunk)
        
        encoded_string.append(new_chunk)
    
    
    encoded_string = encoded_string[::-1]
    
    encoded_string = [-int(c, 16) if len(c) < (bits /4 ) else int(c, 16) for c in encoded_string]
    
    indexes_to_negate = [i for i,j in enumerate(encoded_string) if j < 0]
    
    print("Assembly is:\n")

    # null terminator
    if len(indexes_to_negate) == 0:
        print("        xor " + register + ", " + register)
        print("        push " + register)
    
    encoded_string = [hex(c & (2**bits -1)) for c in encoded_string]
    
    for index, chunk in enumerate(encoded_string):
        print("        mov " + register +", " + chunk)
        
        for i in indexes_to_negate:
            if i == index:
                print("        neg " + register)
                break
        
        print("        push " + register)
    
    print("")
