#!/usr/bin/env python3
"disassembler for 1 bit processor"

import sys

def asHex(num, length=2):
    "formats as hex with zero padding"
    return "{0:#0{1}x}".format(num, length+2) #+2 to account for 0x

def disassm(filename: str) -> bool:
    "Deasseble input binary"
    with open(filename, "rb") as infile:
        print(bcolors.BOLD+"===================================="+bcolors.ENDC)
        PC = 0 # Program counter is byteNo/2
        nops = 0 # Count adjacent nops
        while instruction := infile.read(2):
            instruction = int.from_bytes(instruction, byteorder='big')
            if instruction == 0 and nops:
                if nops == 1:
                    print("...")
                nops += 1
                pass
            elif instruction == 0:
                print(f"{asHex(PC,4)} nop")
                nops = 1
            else:
                nops = 0
                op1 = (instruction & 0x7f00) >> 9
                op2 = (instruction & 0x01fc) >> 2
                ins = bcolors.OKGREEN+"a"+bcolors.ENDC if (instruction & 0x0002) >> 1 else bcolors.HEADER+"c"+bcolors.ENDC
                mag = bcolors.FAIL+"1"+bcolors.ENDC if instruction & 0x0001 else "0"
                print(f"{asHex(PC, 4)}    {ins} {asHex(op1)}, {asHex(op2)}, {mag}     {asHex(instruction, 4)}")
            PC += 1
        return 1 


def main():
    "Lol"
    sys.exit(int(not all(map(disassm, sys.argv[1:]))))

class bcolors:
    "vt100 color codes"
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__":
    main()
