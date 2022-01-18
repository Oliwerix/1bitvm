#!/usr/bin/env python3
"provides the 1 bit virtual machine :D"

import typing
import time
import collections


class VirtM:
    "the main vm class"

    program: bytearray
    regs: list[bool]
    in_buff: typing.Generator[bool, None, None]
    out_buff: collections.deque[bool]
    # TODO pls make stdio support :D

    def __init__(self):
        self.regs = [False] * (2 ** 7)

    def __str__(self):
        return "< Just a tiny vm >"

    def get_reg(self, i: int) -> bool:
        "return register i"
        return self.regs[i]

    def set_reg(self, i: int, val: bool):
        "set register i to val"
        ## TODO
        self.regs[i] = val

    def run(self, after_step=None, itr=-1, delay=-1):
        "run until halt"

        while self.step() and itr != 0:
            itr -= 1
            if callable(after_step):
                after_step(self)
            if delay > 0:
                time.sleep(delay)

    def step(self):
        "Will execute a single instruction"
        prgm_cnt = self.get_pc()
        self.inc_pc()
        inst = self.get_prgm(prgm_cnt)
        opp = inst & 0x2
        adr0 = (inst & 0xFE00) >> 9
        adr1 = (inst & 0x01FC) >> 2
        if opp:
            self.opp1(adr0, adr1)
        else:
            if adr0 == adr1 == 0:
                return True
            self.opp0(adr0, adr1)
        if prgm_cnt == self.get_pc():
            return False
        return True

    def opp0(self, addr1: int, addr2: int):
        "Copy 2 bytes"
        for off in range(16):
            self.set_reg(
                addr2 + off, self.get_reg(addr1 + off) if off < len(self.regs) else True
            )

    def opp1(self, addr1: int, addr2: int):
        "Nand two places, rez to addr2"
        self.set_reg(addr2, not (self.get_reg(addr1) and self.get_reg(addr2)))

    def get_prgm(self, ins: int):
        "get the 'ins' instruction from PRGMEM"
        ins *= 2
        return (
            self.program[ins] << 8 | self.program[ins + 1]
            if ins < len(self.program)
            else 0xFFFF
        )

    def load(self, file_name: str):
        "Load the binary programm proveided in file_name"
        with open(file_name, "rb") as fil:
            self.program = fil.read()
            print(self.program)

    def dump_state(self):
        "Will dump the state of vm to stdout"
        print(f"{self.str_regs()}")

    def dump_command(self):
        "tries to read the currnt command"
        prgm_cnt = self.get_pc()
        inst = self.get_prgm(prgm_cnt)
        opp = "nand" if inst & 0x2 else "copy2b"
        adr0 = (inst & 0xFE00) >> 9
        adr1 = (inst & 0x01FC) >> 2
        print(f"{hex(prgm_cnt)} : ({hex(inst)}): {opp} : {hex(adr0)} -> {hex(adr1)}")

    def dump_all(self):
        "Will dump all!"
        self.dump_command()
        self.dump_state()

    def str_regs(self):
        "'Nicely' format registers for prinitng"
        return f"{ ''.join(map(lambda x:str(int(x)), self.regs)) }"

    def get_pc(self):
        "returns the program counter"
        rez = 0
        for i in range(16):
            rez <<= 1
            rez |= self.get_reg(i)
        return rez

    def inc_pc(self):
        "will increase the programm counter by 1"
        for i in range(15, -1, -1):
            if self.get_reg(i) == 0:
                self.set_reg(i, 1)
                break
            self.set_reg(i, 0)
