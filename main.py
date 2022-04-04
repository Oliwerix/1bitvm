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
    for opt in sys.argv[1:]:
        if opt.startswith("-") and "d" in opt:
            global DEBUG
            DEBUG = True
        else:
            virtual_machine.load(opt)
    if DEBUG:
        virtual_machine.run(-1, dbg, 0.25)
    else:
        virtual_machine.run(-1)


if __name__ == "__main__":
    main()
