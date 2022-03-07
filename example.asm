.org 4
%include "std.asm"

%macro print2 2
    c16 %1, %2, 1
    set_out_b %2 + 0 , 0x14
    set_out_b %2 + 1 , 0x14
    set_out_b %2 + 2 , 0x14
    set_out_b %2 + 3 , 0x14
    set_out_b %2 + 4 , 0x14
    set_out_b %2 + 5 , 0x14
    set_out_b %2 + 6 , 0x14
    set_out_b %2 + 7 , 0x14
    set_out_b %2 + 8 , 0x14
    set_out_b %2 + 9 , 0x14
    set_out_b %2 + 10, 0x14
    set_out_b %2 + 11, 0x14
    set_out_b %2 + 12, 0x14
    set_out_b %2 + 13, 0x14
    set_out_b %2 + 14, 0x14
    set_out_b %2 + 15, 0x14
%endm

word:
.db b"Nig\n"

main:
    print2 labels["word"]  , 0x15
    print2 labels["word"]+1, 0x15
    .org alignto(here,2,0)
    not 0xf
    //c 1, 0, 1

init "main"

