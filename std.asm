%define a nand
%define c copy
%macro print2 2
    c %1, %2, 1
    a %2 + 0, 0x14
    a %2 + 1, 0x14
    a %2 + 2, 0x14
    a %2 + 3, 0x14
    a %2 + 4, 0x14
    a %2 + 5, 0x14
    a %2 + 6, 0x14
    a %2 + 7, 0x14
    a %2 + 8, 0x14
    a %2 + 9, 0x14
    a %2 + 10, 0x14
    a %2 + 11, 0x14
    a %2 + 12, 0x14
    a %2 + 13, 0x14
    a %2 + 14, 0x14
    a %2 + 15, 0x14
%endm
