#!/usr/bin/env python3
# coding:utf-8
import sys

if 'win32' not in sys.platform:
    _BOLD = "\x1b[1m"
    _RESET = "\x1b[0m"
    def BOLD(x): return '{}{}{}'.format(_BOLD, x, _RESET)
else:
    def BOLD(x): return x
