#!/usr/bin/env python3
"main project file"

import sys
import oneb_vm

DEBUG = False


def dbg(x: oneb_vm.VirtM):
    x.dump_state()


def main():
    "What do i put into docstrings?"
    virtual_machine = oneb_vm.VirtM()
    virtual_machine.load("example3.out")
    for opt in sys.argv:
        if opt.startswith("-") and "d" in opt:
            global DEBUG
            DEBUG = True
    if DEBUG:
        virtual_machine.run(-1, dbg, 0.25)
    else:
        virtual_machine.run(-1)


if __name__ == "__main__":
    main()
