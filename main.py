#!/usr/bin/env python3
"main project file?"

import sys
import IPython

import oneb_vm


def main():
    "What do i put into docstrings?"
    virtual_machine = oneb_vm.VirtM()
    virtual_machine.load("example.bin")
    while virtual_machine.step():
        virtual_machine.dump_state()
    for opt in sys.argv:
        if "-i" in opt:
            IPython.embed()


if __name__ == "__main__":
    main()
