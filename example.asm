.org 2
%include "std.asm"

word:
.db b"Bazo "

main:
    print2 labels["word"]  , 0x15
    print2 labels["word"]+2, 0x15

init "main"
