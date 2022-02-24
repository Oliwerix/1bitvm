%define a nand
%define c16 copy
%define nop copy 0,0,0

%macro init 1
    init_tmp:
    .db by2(labels[%1])
    .org 0x0
    c labels["init_tmp"], 0, 1
%endm

%macro get_in 1
get_in_label:
    xor IN_AV, 16-2
    xor 16-2,16-2
%endm

%macro cpy 2
    xor %1,%1
    xor %1,%2
%endm

%macro print2 2
    c16 %1, %2, 1
    a %2 + 0 , 0x14
    a %2 + 1 , 0x14
    a %2 + 2 , 0x14
    a %2 + 3 , 0x14
    a %2 + 4 , 0x14
    a %2 + 5 , 0x14
    a %2 + 6 , 0x14
    a %2 + 7 , 0x14
    a %2 + 8 , 0x14
    a %2 + 9 , 0x14
    a %2 + 10, 0x14
    a %2 + 11, 0x14
    a %2 + 12, 0x14
    a %2 + 13, 0x14
    a %2 + 14, 0x14
    a %2 + 15, 0x14
%endm
