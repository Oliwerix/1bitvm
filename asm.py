#!/usr/bin/env python3
"will aseml da šit"

import sys
import subprocess


def cmp(filename: str) -> bool:
    "compile"
    # TODO add .org
    # // predpostavljam praviln encodng fajla, pa itak je sam asci kj hces sploh pisat notr pac halo
    # Tole je naslabsa koda k sm jo kadar kol napisu -OW
    # subprocess.run(f"nasm -e {filename} > tmp.asm".split(" "), shell=1, check=1)
    with open("tmp.asm", "r") as infile:
        with open(f"{''.join(filename.split('.')[:-1])}.out", "wb") as outfile:
            for line in infile:
                line = line.strip()
                tokens = line.split(" ")
                print(line)
                if len(line) < 3 or line[0] in ["#", "/", "%"]:
                    continue
                if ":" in line:
                    continue
                com = 1 if tokens[0] == "nand" else 0
                # tole je slabo, no sej, a je kej v temu fajlu dobr 😢

                tokens = "".join(tokens[1:]).split(",")
                op1 = eval(tokens[0])
                op2 = eval(tokens[1])
                out = com % 2 << 1
                out += op1 % 128 << 9
                out += op2 % 128 << 2
                outfile.write(out.to_bytes(2, "big"))


def main():
    "I have terminal autism"
    sys.exit(int(not all(map(cmp, sys.argv[1:]))))


if __name__ == "__main__":
    main()
