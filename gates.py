#!/usr/bin/env python3
import itertools


class Op:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Op({self.x},{self.y})"

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.x == other.x


class Oparr:
    def __init__(self, x=None):
        if x != None:
            self.val = x
        else:
            self.val = []

    def copy(self):
        return Oparr(self.val.copy())

    def __str__(self):
        return ",".join(map(str, self.val))

    def __eq__(self, other):
        return isinstance(other, type(self)) and (evl(self.val) == evl(other.val))


def padin(x): return 2**(x) - 1


def nand(A: int, B: int, ln: int) -> int:
    return (~(A & B)) & padin(ln)


def printL(arr):
    arr.sort(key=lambda x: evl(x.val))
    for x, a in enumerate(arr):
        print(
            x, a, tuple(map(lambda x: "{0:0{1}b}".format(x, 2**cln), evl(a.val))))


def evl(arr: list):
    cls = cells.copy()
    for o in arr:
        cls[o.y] = nand(cls[o.x], cls[o.y], 2**cln)
    return cls


def ident(n: int) -> list:
    return [
        int(
            "".join(
                "1" if ((x//(2**a)) % 2) == 0 else "0"
                for x in range(2**n)),
            2
        )
        for a in range(0, n)
    ]


cln = 3
cells = ident(cln)

comb = [Oparr()]

to_do = True
while to_do:
    comb_l = comb.copy()
    print(f"{--*10}{len(comb_l)}:{len(comb_l[-1].val)}")
    # printL(comb_l)
    to_do = False
    opts = range(len(cells))
    for pos in comb_l:
        for x, y in itertools.product(opts, opts):
            bos = pos.copy()
            tmp = Op(x, y)
            bos.val.append(tmp)
            if bos not in comb:
                comb.append(bos)
                to_do = True

print("=="*10)
# printL(filter(lambda x: evl(x.val)[0] == 0b11111111, comb))
# printL(filter(lambda x: evl(x.val)[0] == 0b00000000, comb))
printL(list(filter(lambda x: evl(x.val)[0] == 0b01100110, comb)))
# printL(comb)
print(len(comb), 2**(cln*(2**cln)))
