#!/usr/bin/env pypy3
import itertools


class Op:
    def __init__(self, x, y, m):
        self.x = x
        self.y = y
        self.m = m

    def __str__(self):
        return f"Op({self.x},{self.y},{self.m})"


#    def __eq__(self, other):
#        return isinstance(other, type(self)) and self.x == other.x


class Oparr:
    def __init__(self, x=None):
        if x != None:
            self.val = x
        else:
            self.val = []
        self.update()

    def update(self):
        self.evl = evl(self.val)

    def copy(self):
        return Oparr(self.val.copy())

    def __str__(self):
        return ",".join(map(str, self.val))

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.evl == other.evl)


def padin(x):
    return 2 ** (x) - 1


def nand(A: int, B: int, ln: int) -> int:
    return (~(A & B)) & padin(ln)


def xor(A: int, B: int, ln: int) -> int:
    return (A ^ B) & padin(ln)


def printL(arr):
    # arr.sort(key=lambda x: evl(x.val))
    for x, a in enumerate(arr):
        print(x, a, tuple(map(lambda x: "{0:0{1}b}".format(x, 2**cln), a.evl)))


def evl(arr: list):
    cls = cells.copy()
    for o in arr:
        cls[o.y] = (
            nand(cls[o.x], cls[o.y], 2**cln)
            if o.m == 0
            else xor(cls[o.x], cls[o.y], 2**cln)
        )
    return cls


def ident(n: int) -> list:
    return [
        int(
            "".join("1" if ((x // (2**a)) % 2) == 0 else "0" for x in range(2**n)),
            2,
        )
        for a in range(0, n)
    ]


cln = 2
cells = ident(cln)

comb = [
    Oparr(),
    # Oparr([Op(1,2),Op(1,1),Op(1,2),Op(1,1)])
]

to_do = True
while to_do:
    comb_l = comb.copy()
    print(f"{'--'*10}{len(comb_l)}:{len(comb_l[-1].val)}")
    printL(
        list(filter(lambda x: x.evl[0] == 0b01100110 and x.evl[2] == cells[2], comb))
    )
    # printL(comb_l)
    to_do = False
    opts = range(len(cells))
    for pos in comb_l:
        for x, y in itertools.product(opts, opts):
            for m in range(2):
                bos = pos.copy()
                tmp = Op(x, y, m)
                bos.val.append(tmp)
                bos.update()
                if bos not in comb:
                    comb.append(bos)
                    to_do = True

print("==" * 10)
#printL(filter(lambda x: x.evl[0] == cells[0] and x.evl[1] == cells[0], comb))
printL(filter(lambda x: x.evl[0] == 0b0001, comb))
# printL(list(filter(lambda x: x.evl[0] == 0b01100110, comb)))
# printL(list(filter(lambda x: x.evl[0] == 0b01100110 and x.evl[2] == cells[2], comb)))
print("==" * 10)
printL(comb)
