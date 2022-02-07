#!/usr/bin/env python3
"assembler for 1 bit processor"

import sys
import subprocess

PAGE = 2**7
DEBUG = True


def cmp(filename: str) -> bool:
    "compile"
    nasm = subprocess.run(
        ["nasm", "-e", filename], stdout=subprocess.PIPE, text=True, check=True
    )
    lastjmp = 1
    jumps: dict[str, int] = {}
    with open(f"{''.join(filename.split('.')[:-1])}.out", "w+b") as outfile:

        def write_safe(out: bytes) -> bool:
            "writes int to current position in file, also checks for possible overwriting"
            oli_pojntr = outfile.tell()
            if int.from_bytes(outfile.read(2), "big") != 0:
                print(
                    f"\033[93mOverwriting prevented on {outfile.tell()}\u001b[0m",
                    file=sys.stderr,
                )
                return False
            outfile.seek(oli_pojntr)
            outfile.write(out)
            return True

        print("==" * 10)
        for line in nasm.stdout.splitlines():
            line = line.strip()
            "evaluate python scripts between graves"
            if line.count('`') % 2 == 0 and line.count('`') > 1:
                splitline = line.split('`')
                for i, pyMacro in enumerate(splitline[1::2]):
                    splitline[i*2+1] = str(eval(pyMacro))
                line = ''.join(splitline)
                print(line)
                
            tokens = line.split(" ")
            print(line, tokens)
            if len(line) < 3 or line[0] in ["#", "/", "%"]:
                continue
            if ":" in line:
                line_tokens = line.split(":")
                poz = outfile.tell()
                if DEBUG:
                    print(f"{line_tokens[0]} na {hex(poz)} < {hex(lastjmp)}")
                outfile.seek(lastjmp)
                jumps[line_tokens[0].strip()] = lastjmp
                lastjmp += 1
                write_safe(poz.to_bytes(2, "big"))
                outfile.seek(poz)
                continue
            if ".org" in line:
                org = eval(line.split(".org")[1].strip())
                outfile.seek(org, 0)
                continue
            if ".db" in line:
                data_bin: bytes = eval(line.removeprefix(".db ").strip())
                for part in (data_bin[i : i + 1] for i in range(0, len(data_bin), 4)):
                    write_safe(part)
                if len(data_bin) % 2 != 0:
                    write_safe(bytes((data_bin[len(data_bin) - 1], 0)))
                continue

            # j: typing.Callable[str, int] = lambda arg: jumps[arg]

            com = 1 if tokens[0] == "nand" else 0
            tokens = "".join(tokens[1:]).split(",")
            op1 = eval(tokens[0])
            op2 = eval(tokens[1])
            out = (com % 2) << 1
            # če ni nand in je podan magic bit
            if not com and len(tokens) >= 3 and len(tok_dva := tokens[2].strip()) > 0:
                out |= eval(tok_dva) % 2
            out |= (op1 % 128) << 9
            out |= (op2 % 128) << 2
            outb: bytes = out.to_bytes(2, "big")
            if not write_safe(outb):
                return False
        print("==" * 10)
        return True


def main():
    "I have terminal autism"
    sys.exit(int(not all(map(cmp, sys.argv[1:]))))


if __name__ == "__main__":
    main()
