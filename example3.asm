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
    set1 0x7f
loop_f:
    set1 0x25
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
    do_cell 0x50
    do_cell 0x51
    do_cell 0x52
    do_cell 0x53
    do_cell 0x54
    do_cell 0x55
    do_cell 0x56
    do_cell 0x57
    do_cell 0x58
    do_cell 0x59
    do_cell 0x5a
    do_cell 0x5b
    do_cell 0x5c
    do_cell 0x5d
    do_cell 0x5e
    do_cell 0x5f
    do_cell 0x60
    do_cell 0x61
    do_cell 0x62
    do_cell 0x63
    do_cell 0x64
    do_cell 0x65
    do_cell 0x66
    do_cell 0x67
    do_cell 0x68
    do_cell 0x69
    do_cell 0x6a
    do_cell 0x6b
    do_cell 0x6c
    do_cell 0x6d
    do_cell 0x6e
    do_cell 0x6f
    do_cell 0x70
    do_cell 0x71
    do_cell 0x72
    do_cell 0x73
    do_cell 0x74
    do_cell 0x75
    do_cell 0x76
    do_cell 0x77
    do_cell 0x78
    do_cell 0x79
    do_cell 0x7a
    do_cell 0x7b
    do_cell 0x7c
    do_cell 0x7d
    do_cell 0x7e
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
    print_cell 0x50
    print_cell 0x51
    print_cell 0x52
    print_cell 0x53
    print_cell 0x54
    print_cell 0x55
    print_cell 0x56
    print_cell 0x57
    print_cell 0x58
    print_cell 0x59
    print_cell 0x5a
    print_cell 0x5b
    print_cell 0x5c
    print_cell 0x5d
    print_cell 0x5e
    print_cell 0x5f
    print_cell 0x60
    print_cell 0x61
    print_cell 0x62
    print_cell 0x63
    print_cell 0x64
    print_cell 0x65
    print_cell 0x66
    print_cell 0x67
    print_cell 0x68
    print_cell 0x69
    print_cell 0x6a
    print_cell 0x6b
    print_cell 0x6c
    print_cell 0x6d
    print_cell 0x6e
    print_cell 0x6f
    print_cell 0x70
    print_cell 0x71
    print_cell 0x72
    print_cell 0x73
    print_cell 0x74
    print_cell 0x75
    print_cell 0x76
    print_cell 0x77
    print_cell 0x78
    print_cell 0x79
    print_cell 0x7a
    print_cell 0x7b
    print_cell 0x7c
    print_cell 0x7d
    print_cell 0x7e
    c labels["newl"], 0x15, 1
    printc_m 0x15,0x14
c labels["loop"],0,1

.org labels["pCell"]*2
.db by2(labels["print_cells"])
.org labels["loop"]*2
.db by2(labels["loop_f"])


init "main"
