#!/usr/bin/env python3
"provides the 1 bit virtual machine :D"

import typing
import time

# import collections

IN = 0x10
IN_A = 0x11
OU = 0x12
OU_A = 0x13


class Bcolors:
    "vt100 color codes"
    HEADER = "\033[35m"
    OKBLUE = "\033[34m"
    OKCYAN = "\033[36m"
    OKGREEN = "\033[32m"
    WARNING = "\033[33m"
    FAIL = "\033[31m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Hook:
    "creates a RAM hook"

    def __init__(self):
        pass

    def evl(self, that, cell: int, write: bool, data: bool):
        "eval a hook instead of read or write op"

    def flush(self, that):
        "flush je hook implemented"


class STDOUT(Hook):
    "ram HOOK for writing"
    buff: list[bool]

    def __init__(self):
        super().__init__()
        self.buff = []

    def evl(self, that, cell: int, write: bool, data: bool):
        "eval for hook"
        if write:
            if data:
                self.buff.append(that.get(OU))
                self.flush(that)
                # print(f"--> {self.buff}")
        return False

    def flush(self, that):
        "try to flush the buffer"
        while len(self.buff) >= 8:
            out: int = 0
            for _ in range(8):
                out <<= 1
                out |= self.buff.pop(0)
            print(out.to_bytes(1, "big").decode(), end="")


class STDIN(Hook):
    "ram HOOK for reading"
    buff: list[bool]

    def __init__(self):
        super().__init__()
        self.buff = []

    def evl(self, that, cell: int, write: bool, data: bool):
        "eval for hook"
        # print(f"<-- {self.buff}")
        if not self.buff:
            self.flush(that)
        if not write:
            return bool(self.buff)
        if not data:
            if self.buff:
                self.nxt(that)
            return self.buff

    def nxt(self, that):
        "set the next buff to bit"
        self.buff.pop(0)
        if self.buff:
            that.set(IN, self.buff[0])

    def flush(self, that):
        "try to flush the buffer"
        inp = input(">").encode()
        if len(inp) > 0:
            self.buff = [bool(x & (1 << y)) for x in inp for y in range(7, -1, -1)]
            that.set(IN, self.buff[1])


class RAM:
    "onebit ram storage and managment class"
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
        return self.gimmi_regs()

    def gimmi_regs(self):
        "nice formaty action"
        return f"{ ''.join(map(lambda x:str(int(x)), self.regs)) }"

    def set_hooks(self, hooks: dict[tuple[int, bool], Hook]):
        "bind a hook dict"
        self.hooks = hooks

    def get_hooks(self) -> dict[tuple[int, bool], Hook]:
        "get the current hooks dict"
        return self.hooks

    def evl_hooks(self, reg: int, to_regs: bool, data: bool) -> bool:
        "run necesary hooks"
        return self.hooks[(reg, to_regs)].evl(self, reg, to_regs, data)

    def get(self, i: int) -> bool:
        "return register i"
        if (i, False) in self.hooks:
            return self.evl_hooks(i, False, False)
        return self.regs[i]

    def set(self, i: int, val: bool):
        "set register i to val"
        if (i, True) in self.hooks:
            self.evl_hooks(i, True, val)
        else:
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
            if self.get(i) == False:
                self.set(i, True)
                break
            self.set(i, False)


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
        opp = inst & 0x2
        adr0 = (inst & 0xFE00) >> 9
        adr1 = (inst & 0x01FC) >> 2
        meta = inst & 0x1
        if opp:
            if meta:
                opps = "xor "
            else:
                opps = "nand"
        else:
            if meta:
                opps = "cppm"
            else:
                opps = "copy"
        print(f"{hex(ins)} : {opps} : {hex(adr0)} -> {hex(adr1)}")

    def get(self, i: int) -> int:
        "get the 'i' instruction from PRGMEM"
        i *= 2
        return self.prgm[i] << 8 | self.prgm[i + 1] if i < len(self.prgm) else 0

    def set(self, i: int, val: bytes):
        "set mem at adress"
        print(f"    {i}:{self.get(i)!r} not set to {val!r}")
        assert False, "Not implemented!"


class VirtM:
    "the main vm class"

    pgm: PGM
    ram: RAM

    def __init__(self):
        self.ram = RAM(7)
        hook_in = STDIN()
        hook_out = STDOUT()
        self.ram.set_hooks(
            {
                (IN_A, False): hook_in,
                (IN_A, True): hook_in,
                (OU_A, False): hook_out,
                (OU_A, True): hook_out,
            }
        )
        self.pgm = PGM()

    def __str__(self):
        return "[ ._. ] <( Prosim ne printaj me)"

    def load(self, filename: str):
        "load programm to machine"
        self.pgm.load(filename)

    def run(self, itr: int = -1, after_step: typing.Callable = None, delay: int = -1):
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
        meta = inst & 0x1
        if opp:
            self.opp1(adr0, adr1, meta)
        else:
            if adr0 == adr1 == 0:
                return True
            self.opp0(adr0, adr1, meta)
        if prgm_cnt == self.ram.get_pc():
            print("---")
            return False
        return True

    def opp0(self, addr1: int, addr2: int, meta: int):
        "Copy 2 bytes"
        buff: list[bool] = []
        if not meta:
            for off in range(16):
                buff.append(self.ram.get(addr1 + off))
        else:
            data = self.pgm.get(addr1)
            for off in range(16):
                buff.insert(0, bool(data & 1))
                data >>= 1
        for off in range(16):
            self.ram.set(addr2 + off, buff.pop(0))

    def opp1(self, addr1: int, addr2: int, meta: int):
        "Nand two places, rez to addr2"
        # breakpoint()
        self.ram.set(
            addr2,
            (not (self.ram.get(addr1) and self.ram.get(addr2)))
            if not meta
            else (self.ram.get(addr1) ^ self.ram.get(addr2)),
        )

    def dump_state(self):
        "Will dump the state of vm to stdout"
        command = self.ram.get_pc()
        self.pgm.dump_command(command)
        # print(format(self.ram.get_pc(), "0=4x"), end=":")
        print(self.ram)
