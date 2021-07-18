#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import time
import pstats
import cProfile

def do_something():
    time.sleep(3)
    re.compile("aaa|bbb")

prof = cProfile.Profile()
prof.enable()

do_something()

prof.disable()
prof.create_stats()
prof.dump_stats("./out.prof")

# prof.print_stats()
p = pstats.Stats(prof)
p.sort_stats('tottime').print_stats(20)



