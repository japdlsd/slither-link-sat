#!/usr/bin/python3

import common
from common import HumanReadableOutput

def errprint(*args):
    """General debug messages."""
    common.errprint("solv1.py: ", *args)

def solve(rawInput):
    # @TODO
    errprint("Starting...")
    return HumanReadableOutput(rawInput, [])
