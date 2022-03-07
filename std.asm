%define a nand
%define c16 copy
%define nop copy 0,0,0

%macro not 1
    a %1,%1
%endm

%macro init 1
    .org 2
    .db by2(labels[%1])
    .org 0
    c 1, 0, 1
%endm

    ;; wait for (reg), trash
%macro wait_for 2
    //waitfor
    .org alignto(here,4,0)
    cpy %1, %2
    not %2
    a %2, 13
%endm

%macro wait_forn 2
    //waitforn
    .org alignto(here,4,0)
    cpy %1, %2
    nop
    a %2, 13
%endm

    ;; input, trash
%macro set_out_b 2
    //setoutb
    wait_forn OU_A, %2
    cpy %1,OU
    not OU_A
%endm
    ;; output, trash
%macro get_in_b 2
    //getinb
    wait_for IN_A, %2
    cpy IN, %1
%endm

%macro cpy 2
    xor %2,%2
    xor %1,%2
%endm

