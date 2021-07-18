#!/usr/bin/python3
# -*- coding: utf-8 -*-
import line_profiler
import time
import sys

def do_something():
    time.sleep(1)
    for i in range(0, 3):
        print(i**2)
    print('end')

profile = line_profiler.LineProfiler(do_something) 
profile.enable()  # 开始分析

do_something()

profile.disable()  # 停止分析
profile.print_stats(sys.stdout) 
