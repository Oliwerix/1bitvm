#!/usr/bin/env python3
"provides the 1 bit virtual machine :D"

import typing
import time

# import collections


class Hook:
    "creates a RAM hook"

    def __inin__(self):
        pass

    def evl(self, cell: int, write: bool):
        pass


class RAM:
    "onebit ram storage and managment class"
    # TODO make stdio
    # in_buff: typing.Generator[bool, None, None]
    # out_buff: collections.deque[bool]
    regs: list[bool]
    hooks: dict[tuple[int, bool], Hook]

    def __init__(self, addr_spc: int = 1):
        assert addr_spc > 0, "Opala, mau neki ti ne gre ram"
        self.regs = [False] * (2**addr_spc)

    def __len__(self) -> int:
        return len(self.regs)

    def __str__(self):
        "'Nicely' format registers for prinitng"
        return f"{ ''.join(map(lambda x:str(int(x)), self.regs)) }"

    def set_hooks(self, hooks: dict[tuple[int, bool], Hook]):
        "bind a hook dict"
        self.hooks = hooks

    def get_hooks(self) -> dict[tuple[int, bool], Hook]:
        "get the current hooks dict"
        return self.hooks

    def run_hooks(self, reg: int, to_regs: bool):
        "run necesary hooks"
        if (reg, to_regs) in self.hooks:
            # TODO
            pass

    def get(self, i: int) -> bool:
        "return register i"
        self.run_hooks(i, False)
        return self.regs[i]

    def set(self, i: int, val: bool):
        "set register i to val"
        self.run_hooks(i, True)
        self.regs[i] = val

    def get_pc(self) -> int:
        "returns the program counter"
        rez = 0
        for i in range(16):
            rez <<= 1
            rez |= self.get(i)
        return rez

    def inc_pc(self):
        "will increase the programm counter by 1"
        for i in range(15, -1, -1):
            if self.get(i) == 0:
                self.set(i, 1)
                break
            self.set(i, 0)


class PGM:
    "Programm memory storage class"
    prgm: bytearray

    def __init__(self):
        self.prgm = None

    def load(self, file_name: str):
        "Load the binary programm proveided in file_name"
        with open(file_name, "rb") as fil:
            self.prgm = bytearray(fil.read())

    def dump_command(self, ins: int):
        "tries to read the currnt command"
        inst = self.get(ins)
        opp = "nand" if inst & 0x2 else "copy2b"
        adr0 = (inst & 0xFE00) >> 9
        adr1 = (inst & 0x01FC) >> 2
        print(f"{hex(ins)} : {opp} : {hex(adr0)} -> {hex(adr1)}")

    def get(self, i: int):
        "get the 'i' instruction from PRGMEM"
        i *= 2
        return self.prgm[i] << 8 | self.prgm[i + 1] if i < len(self.prgm) else 0

    def set(self, i: int, val: bytes):
        "set mem at adress"
        assert False, "Not implemented!"


class VirtM:
    "the main vm class"

    pgm: PGM
    ram: RAM

    def __init__(self):
        self.ram = RAM(7)
        self.pgm = PGM()

    def __str__(self):
        return "[ ._. ] <( Prosim ne printaj me)"

    def load(self, filename: str):
        "load programm to machine"
        self.pgm.load(filename)

    def run(self, after_step: typing.Callable = None, itr: int = -1, delay: int = -1):
        "run until halt"

        while self.step() and itr != 0:
            itr -= 1
            if callable(after_step):
                after_step(self)
            if delay > 0:
                time.sleep(delay)

    def step(self):
        "Will execute a single instruction"
        prgm_cnt = self.ram.get_pc()
        self.ram.inc_pc()
        inst = self.pgm.get(prgm_cnt)
        opp = inst & 0x2
        adr0 = (inst & 0xFE00) >> 9
        adr1 = (inst & 0x01FC) >> 2
        if opp:
            self.opp1(adr0, adr1)
        else:
            if adr0 == adr1 == 0:
                return True
            self.opp0(adr0, adr1)
        if prgm_cnt == self.ram.get_pc():
            return False
        return True

    # TODO bring opps up to spec!
    def opp0(self, addr1: int, addr2: int):
        "Copy 2 bytes"
        for off in range(16):
            self.ram.set(
                addr2 + off,
                self.ram.get(addr1 + off) if off < len(self.ram) else True,
            )

    def opp1(self, addr1: int, addr2: int):
        "Nand two places, rez to addr2"
        self.ram.set(addr2, not (self.ram.get(addr1) and self.ram.get(addr2)))

    def dump_state(self):
        "Will dump the state of vm to stdout"
        self.pgm.dump_command(self.ram.get_pc())
        print(format(self.ram.get_pc(), "0=4x"), end=":")
        print(self.ram)
