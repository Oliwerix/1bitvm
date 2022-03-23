.org 4
pCell:
    .db b"\000\000"
loop:
    .db b"\000\000"

%include "std.asm"

znaka:
    .db b"#"
newl:
    .db b"\n"

%macro eval_cell 1
    a 2+%1, 0+%1
    a 1+%1, 0+%1
    a 2+%1, 0+%1
    x 1+%1, 0+%1
    a 0+%1, 0+%1
%endm

%macro do_cell 1
    cpy 0x26,0x25
    cpy 0x27,0x26
    cpy %1+1,0x27
    eval_cell 0x25
    cpy 0x25, %1
%endm

main:
    set1 0x4f
loop_f:
    set0 0x25
    set0 0x26
    set0 0x27
    do_cell 0x2f
    do_cell 0x30
    do_cell 0x31
    do_cell 0x32
    do_cell 0x33
    do_cell 0x34
    do_cell 0x35
    do_cell 0x36
    do_cell 0x37
    do_cell 0x38
    do_cell 0x39
    do_cell 0x3a
    do_cell 0x3b
    do_cell 0x3c
    do_cell 0x3d
    do_cell 0x3e
    do_cell 0x3f
    do_cell 0x40
    do_cell 0x41
    do_cell 0x42
    do_cell 0x43
    do_cell 0x44
    do_cell 0x45
    do_cell 0x46
    do_cell 0x47
    do_cell 0x48
    do_cell 0x49
    do_cell 0x4a
    do_cell 0x4b
    do_cell 0x4c
    do_cell 0x4d
    do_cell 0x4e
    do_cell 0x4f
    c labels["pCell"],0,1



%macro print_cell 1
    //.org alignto(here,)
    c labels["znaka"],0x15,1
    cpy %1, 0x19

    printc_m 0x15,0x14
%endm

print_cells:
    print_cell 0x30
    print_cell 0x31
    print_cell 0x32
    print_cell 0x33
    print_cell 0x34
    print_cell 0x35
    print_cell 0x36
    print_cell 0x37
    print_cell 0x38
    print_cell 0x39
    print_cell 0x3a
    print_cell 0x3b
    print_cell 0x3c
    print_cell 0x3d
    print_cell 0x3e
    print_cell 0x3f
    print_cell 0x40
    print_cell 0x41
    print_cell 0x42
    print_cell 0x43
    print_cell 0x44
    print_cell 0x45
    print_cell 0x46
    print_cell 0x47
    print_cell 0x48
    print_cell 0x49
    print_cell 0x4a
    print_cell 0x4b
    print_cell 0x4c
    print_cell 0x4d
    print_cell 0x4e
    print_cell 0x4f
    c labels["newl"], 0x15, 1
    printc_m 0x15,0x14
c labels["loop"],0,1

.org labels["pCell"]*2
.db by2(labels["print_cells"])
.org labels["loop"]*2
.db by2(labels["loop_f"])


init "main"
