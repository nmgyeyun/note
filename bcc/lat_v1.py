#!/usr/bin/python
#
# vfsreadlat.py		VFS read latency distribution.
#			For Linux, uses BCC, eBPF. See .c file.
#
# Written as a basic example of a function latency distribution histogram.
#
# USAGE: vfsreadlat.py [interval [count]]
#
# The default interval is 5 seconds. A Ctrl-C will print the partially
# gathered histogram then exit.
#
# Copyright (c) 2015 Brendan Gregg.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# 15-Aug-2015	Brendan Gregg	Created this.

from __future__ import print_function
from bcc import BPF
from ctypes import c_ushort, c_int, c_ulonglong
from time import sleep
from sys import argv
#import fire 


# load BPF program
b = BPF(src_file = "lat_v1.c")
b.attach_uprobe(name="/home/note/bcc/test", sym="func_test_lat", fn_name="do_entry")
b.attach_uretprobe(name="/home/note/bcc/test", sym="func_test_lat", fn_name="do_return")

# header
print("Tracing... Hit Ctrl-C to end.")

def main():
    # header
    print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMM", "PID", "MESSAGE"))

    # format output
    while 1:
        try:
            (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        except ValueError:
            continue
        print("%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
        #(api, i) = msg.split()


if __name__ == '__main__':
  # fire.Fire()
  main()
