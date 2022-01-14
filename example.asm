#define a nand
#define c copy
#define cpy(a,b) \
    a 0, b\
    a a, b\
    a b, b


main:
    a 0x7f, 0x7f
    cpy(0x7f,0x7c)
    c 0x10, 0x0
