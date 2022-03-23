.org 4
%include "std.asm"

main:
    get_in_b 0x20,0x21
    set_out_b 0x20,0x21
    not IN_A
    c 1, 0, 1

init "main"
