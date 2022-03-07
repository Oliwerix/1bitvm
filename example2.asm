.org 4
%include "std.asm"

main:
    //nand 0x2f,0x2f
    get_in_b 0x20,0x21
    set_out_b 0x20,0x21
    not IN_A
    c 1, 0, 1
    //get_in 32

init "main"
