%define a nand
%define c copy
%macro cpy 2
    a 0, %2
    a %1, %2
    a %2, %2
%endmacro


main:
    a 0x7f, 0x7f
    cpy 0x7f,0x7c
    c 0x10, 0x0
