#!/usr/bin/python3
import cProfile
import re

def foo():
    for a in range(0, 101):
        for b in range(0, 101):
            if a + b == 100:
                yield a, b



foo()

