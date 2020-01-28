#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
filename = 'examples/mult.ls8'
cpu.load(filename)
cpu.run()