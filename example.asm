.org PAGE
%include "std.asm"

word:
.db b"Bazo "

main:
    print2 jumps["word"]  , 0x15
    print2 jumps["word"]+2, 0x15

.org 0x0
c j("main"), 0, 1
