#!/usr/bin/env python3
"main project file?"

import sys
import IPython

import oneb_vm


def main():
    "What do i put into docstrings?"
    virtual_machine = oneb_vm.VirtM()
    virtual_machine.ram.set_hooks({})
    virtual_machine.load("example2.out")
    virtual_machine.run(lambda x: x.dump_state(), 20, 2)
    # :D
    for opt in sys.argv:
        if "i" in opt:
            IPython.embed()


if __name__ == "__main__":
    main()
