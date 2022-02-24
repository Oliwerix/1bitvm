.org 2
%include "std.asm"

main:
    nand 0x2f,0x2f
loop:
    nop

    .orgr 2
jumper:
    .db by2(labels["loop"])
    .orgr -4
    c labels["jumper"], 0, 1
    .orgr 2
    //get_in 32

init "main"
