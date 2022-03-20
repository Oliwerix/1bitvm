#!/usr/bin/env python3
"assembler for 1 bit processor"

import sys
import subprocess
import typing
import math

PAGE = 2**7
DEBUG = False

IN = 0x10
IN_A = 0x11
OU = 0x12
OU_A = 0x13


def write_safe(outfile: typing.IO, data: bytes) -> bool:
    "writes int to current position in file, also checks for possible overwriting"
    oli_pojntr = outfile.tell()
    assert len(data) == 2, "Something wong!"
    if int.from_bytes(outfile.read(2), "big") != 0:
        print(
            f"\033[33mOverwriting prevented on {outfile.tell()//2:#06x}\033[0m",
            file=sys.stderr,
        )
        return False
    outfile.seek(oli_pojntr)
    outfile.write(data)
    return True


def py_eval(line: str, loc: dict):
    "eval py regions in lines"
    if line.count("<py>") % 2 == 0 and line.count("<py>") > 1:
        # breakpoint()
        splitline = line.split("<py>")
        for i, py_macro in enumerate(splitline[1::2]):
            splitline[i * 2 + 1] = str(eval(py_macro, globals(), loc))
        return "".join(splitline)
    return line


def write_inst(outfile: typing.IO, line: str, loc: dict) -> bool:
    "interpret line and write as instruction"
    outfile.seek(math.ceil((outfile.tell() % 2) / 2), 1)
    tokens = line.split(" ")
    xor = 0
    if tokens[0] == "xor":
        com = 1
        xor = 1
    else:
        com = 1 if tokens[0] == "nand" else 0
    tokens = tuple(map(str.strip, "".join(tokens[1:]).split(",")))
    op1 = eval(tokens[0], globals(), loc)
    op2 = eval(tokens[1], globals(), loc)
    out = (com % 2) << 1
    if len(tokens) >= 3 and len(tokens[2]) > 0:
        out |= eval(tokens[2], globals(), loc) % 2
    if xor:
        out |= 1
    out |= (op1 % 128) << 9
    out |= (op2 % 128) << 2
    outb: bytes = out.to_bytes(2, "big")
    if not write_safe(outfile, outb):
        return False
    return True


def alignto(here: int, length: int, pattern: int):
    "align PC to next pattern"
    mask: int = 2**length - 1
    if here & mask <= pattern:
        return here & ~mask | pattern & mask
    return (((here >> length) + 1) << length) & ~mask | pattern & mask


def by2(arg: int) -> bytes:
    "helper function that casts ints(?) to 2 bytes"
    return arg.to_bytes(2, "big")


def cmp(filename: str) -> bool:
    "compile"
    nasm = subprocess.run(
        ["nasm", "-e", filename], stdout=subprocess.PIPE, text=True, check=True
    )
    labels: dict[str, int] = {}
    fail: bool = False
    with open(f"{''.join(filename.split('.')[:-1])}.out", "w+b") as outfile:
        print("==" * 3 + filename + "==" * 3)
        for num, line in enumerate(nasm.stdout.splitlines()):
            line = line.strip()
            here = outfile.tell()
            line = py_eval(line, locals())
            if DEBUG:
                print(f"{num:6d} : {here//2:#6x} : {line}")
            if (
                len(line) < 3 or (line[0] in ["#", "/", "%"]) or line == "None"
            ):  # ignore
                continue
            if ":" in line:  # label
                label_name = line.split(":")[0].strip()
                poz = outfile.tell() // 2
                if DEBUG:
                    print(f"{label_name} na {poz:#06x}")
                labels[label_name] = poz
            elif ".orgr" in line:  # jump in out file
                org = eval(line.removeprefix(".orgr").strip())
                outfile.seek(org, 1)
            elif ".org" in line:  # jump in out file
                org = eval(line.removeprefix(".org").strip())
                outfile.seek(org)
            elif ".db" in line:  # binary data dump
                data_bin: bytes = eval(line.removeprefix(".db ").strip())
                for part in (data_bin[i : i + 2] for i in range(0, len(data_bin), 2)):
                    if len(part) < 2:
                        part = part + b"\x00"
                    write_safe(outfile, part)
            else:  # assume instruction
                fail = not write_inst(outfile, line, locals())
            # j: typing.Callable[str, int] = lambda arg: jumps[arg]
            if fail:
                # print(nasm.stdout)
                return False

        return True


def main():
    "I have terminal autism"
    for opt in sys.argv:
        if opt.startswith("-") and "d" in opt:
            global DEBUG
            DEBUG = True
        if opt.startswith("-") and "n" in opt:
            return
    sys.exit(
        int(not all(map(cmp, filter(lambda x: not x.startswith("-"), sys.argv[1:]))))
    )


if __name__ == "__main__":
    main()
