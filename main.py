#!/usr/bin/env python3
"main project file?"

import sys

# import IPython

import oneb_vm

DEBUG = False


def main():
    "What do i put into docstrings?"
    virtual_machine = oneb_vm.VirtM()
    virtual_machine.load("example2.out")
    # :D
    for opt in sys.argv:
        if opt.startswith("-") and "d" in opt:
            global DEBUG
            DEBUG = True
        # if opt.startswith("-") and "i" in opt:
        # IPython.embed()
    if DEBUG:
        virtual_machine.run(210, lambda x: x.dump_state())
    else:
        virtual_machine.run(-1)


if __name__ == "__main__":
    main()
