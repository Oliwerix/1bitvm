#!/usr/bin/env python3
"assembler for 1 bit processor"

import sys
import subprocess
import typing


def cmp(filename: str) -> bool:
    "compile"
    # TODO rabmo .db
    # TODO rabmo advanced preprocessor motione
    nasm = subprocess.run(["nasm", "-e", filename], stdout=subprocess.PIPE, text=True)
    outs = nasm.stdout
    with open(f"{''.join(filename.split('.')[:-1])}.out", "w+b") as outfile:

        def writeInstruction(out: int, noBytes: int = 2) -> bool:
            "writes int to current position in file, also checks for possible overwriting"
            if int.from_bytes(outfile.read(noBytes), "big") != 0:
                print(
                    f"\033[93mOverwriting prevented on {outfile.tell()}\u001b[0m",
                    file=sys.stderr,
                )
                return False
            outfile.write(out.to_bytes(noBytes, "big"))
            return True

        print("--" * 10)
        for line in outs.splitlines():
            line = line.strip()
            tokens = line.split(" ")
            print(line)
            if len(line) < 3 or line[0] in ["#", "/", "%"]:
                continue
            if ":" in line:
                continue
            if ".org" in line:
                org = line.split(".org")[1].strip()
                outfile.seek(eval(org), 0)
                continue
            com = 1 if tokens[0] == "nand" else 0
            tokens = "".join(tokens[1:]).split(",")
            op1 = eval(tokens[0])
            op2 = eval(tokens[1])
            out = com % 2 << 1
            out += op1 % 128 << 9
            out += op2 % 128 << 2
            if not writeInstruction(out):
                return False
        print("--" * 10)
        return True


def main():
    "I have terminal autism"
    sys.exit(int(not all(map(cmp, sys.argv[1:]))))


if __name__ == "__main__":
    main()
