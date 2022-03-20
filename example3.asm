.org 4
%include "std.asm"

znaka:
    .db b"#"
    .db b"."
newl:
    .db b"\n"

main:
    set1 0x30
    set1 0x31
    set0 0x32
    add 0x30,0x31,0x32
    .org alignto(here,2, 0)
    not 0xf
    //c labels["znaka"], 0x15, 1
    //call "printc"
    //c labels["znaka"], 0x15, 1
    //c 0x15+8, 0x15
    //call "printc"
    //c labels["newl"], 0x15, 1
    //call "printc"
    c 1,0,1


init "main"
