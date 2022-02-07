#!/usr/bin/env python3
"assembler for 1 bit processor"

import sys
import subprocess
import typing

PAGE = 2**7


def cmp(filename: str) -> bool:
    "compile"
    nasm = subprocess.run(["nasm", "-e", filename], stdout=subprocess.PIPE, text=True)
    outs = nasm.stdout
    lastjmp = 1
    jumps: dict[str, int] = dict()
    with open(f"{''.join(filename.split('.')[:-1])}.out", "w+b") as outfile:

        def writeSafe(out: bytes) -> bool:
            "writes int to current position in file, also checks for possible overwriting"
            Oli_pojntr = outfile.tell()
            if int.from_bytes(outfile.read(2), "big") != 0:
                print(
                    f"\033[93mOverwriting prevented on {outfile.tell()}\u001b[0m",
                    file=sys.stderr,
                )
                return False
            outfile.seek(Oli_pojntr)
            outfile.write(out)
            return True

        print("==" * 10)
        for line in outs.splitlines():
            line = line.strip()
            tokens = line.split(" ")
            print(line)
            if len(line) < 3 or line[0] in ["#", "/", "%"]:
                continue
            if ":" in line:
                ln = line.split(":")
                poz = outfile.tell()
                print(f"{ln[0]} na {hex(poz)} < {hex(lastjmp)}")
                outfile.seek(lastjmp)
                jumps[ln[0].strip()] = lastjmp
                lastjmp += 1
                writeSafe(poz.to_bytes(2, "big"))
                outfile.seek(poz)
                continue
            if ".org" in line:
                org = eval(line.split(".org")[1].strip())
                outfile.seek(org, 0)
                continue
            if ".db" in line:

                db: bytes = eval(line.split(".db")[1].strip())
                for gg in (db[i : i + 1] for i in range(0, len(db), 4)):
                    writeSafe(gg)
                if len(db) % 2 != 0:
                    writeSafe(bytes((db[len(db) - 1], 0)))
                continue

            def j(arg: str) -> int:
                return jumps[arg]

            com = 1 if tokens[0] == "nand" else 0
            tokens = "".join(tokens[1:]).split(",")
            op1 = eval(tokens[0])
            op2 = eval(tokens[1])
            out = (com % 2) << 1
            if not com and len(tokens) >= 3:
                out |= eval(tokens[2]) % 2
            out |= (op1 % 128) << 9
            out |= (op2 % 128) << 2
            outb: bytes = out.to_bytes(2, "big")
            if not writeSafe(outb):
                return False
        print("==" * 10)
        return True


def main():
    "I have terminal autism"
    sys.exit(int(not all(map(cmp, sys.argv[1:]))))


if __name__ == "__main__":
    main()
