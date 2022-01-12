#!/usr/bin/env python3
"provides the 1 bit virtual machine :D"


class VirtM:
    "the main vm class"

    program: bytearray
    regs: list[bool]
    in_buff: list[bool]
    out_buff: list[bool]
    # TODO pls make stdio support :D

    def __init__(self):
        self.regs = [False] * (2 ** 7)

    def __str__(self):
        return "< Just a tiny vm >"

    def run(self):
        "run until halt"
        while self.step():
            pass

    def step(self):
        "Will execute a single instruction"
        prgm_cnt = self.get_pc()
        self.inc_pc()
        inst = self.get_prgm(prgm_cnt)
        opp = inst & 0x2
        adr0 = inst & 0xFE00
        adr1 = inst & 0x01FC
        if opp:
            self.opp1(adr0, adr1)
        else:
            if adr0 == adr1 == 0:
                return False
            self.opp0(adr0, adr1)
        return True

    def opp0(self, addr1: int, addr2: int):
        "Copy 2 bytes"
        for off in map(lambda x: x + addr2, range(16)):
            self.regs[addr1] = self.regs[off] if off < len(self.regs) else True

    def opp1(self, addr1: int, addr2: int):
        "Nand two places, rez to addr2"
        self.regs[addr2] = not (self.regs[addr1] and self.regs[addr2])

    def get_prgm(self, ins: int):
        "get the 'ins' instruction from PRGMEM"
        return (
            self.program[ins] << 8 | self.program[ins + 1]
            if ins * 2 < len(self.program)
            else 0
        )

    def load(self, file_name: str):
        "Load the binary programm proveided in file_name"
        with open(file_name, "rb") as fil:
            self.program = fil.read()

    def dump_state(self):
        "Will dump the state of vm to stdout"
        print(f"{self.str_regs()}")

    def str_regs(self):
        "'Nicely' format registers for prinitng"
        return f"{ ''.join(map(lambda x:str(int(x)), self.regs)) }"

    def get_pc(self):
        "returns the program counter"
        rez = 0
        for i in range(16):
            rez <<= 1
            rez |= self.regs[i]
        return rez

    def inc_pc(self):
        "will increase the programm counter by 1"
        for i in range(15, -1, -1):
            if self.regs[i] == 0:
                self.regs[i] = 1
                break
            self.regs[i] = 0
