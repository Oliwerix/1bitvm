#!/usr/bin/env python3
"disassembler for 1 bit processor"

import sys


def as_hex(num, length=2):
    "formats as hex with zero padding"
    return "{0:#0{1}x}".format(num, length + 2)  # +2 to account for 0x


def disassm(filename: str) -> bool:
    "Deasseble input binary"
    with open(filename, "rb") as infile:
        print(Bcolors.BOLD + "==" * 3 + filename + "==" * 3 + Bcolors.ENDC)
        pc = 0  # Program counter is byteNo/2
        nops = 0  # Count adjacent nops
        while instruction := infile.read(2):
            instruction = int.from_bytes(instruction, byteorder="big")
            if instruction == 0 and nops:
                if nops == 1:
                    print("...")
                nops += 1
            elif instruction == 0:
                print(f"{as_hex(pc,4)} nop")
                nops = 1
            else:
                nops = 0
                op1 = (instruction & 0x7F00) >> 9
                op2 = (instruction & 0x01FC) >> 2
                ins = (
                    Bcolors.OKGREEN + "a" + Bcolors.ENDC
                    if (instruction & 0x0002) >> 1
                    else Bcolors.HEADER + "c" + Bcolors.ENDC
                )
                mag = Bcolors.FAIL + "1" + Bcolors.ENDC if instruction & 0x0001 else "0"
                print(
                    f"{as_hex(pc, 4)}    {ins} {as_hex(op1)}, {as_hex(op2)}, {mag}     {as_hex(instruction, 4)}"
                )
            pc += 1
        return 1


def main():
    "aftizem inc"
    sys.exit(
        int(
            not all(map(disassm, filter(lambda x: not x.startswith("-"), sys.argv[1:])))
        )
    )


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


if __name__ == "__main__":
    main()
