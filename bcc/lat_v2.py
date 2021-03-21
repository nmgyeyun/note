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
import argparse


# arguments
examples = """examples:
    ./lat_v2                 # ... trace all process use idl
    ./lat_v2 -p 185          # ... trace PID 185, output top10
    ./lat_v2 -p 185 -t 10    # ... trace PID 185, output top10
    ./lat_v2 -p 185 -t 10 -i 5    # ... trace PID 185, output top10 every 5 seconds
"""
parser = argparse.ArgumentParser(
    description="Trace and print idl call latency",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=examples)
parser.add_argument("-p", "--pid", help="trace this PID only")
parser.add_argument("-t", "--top", help="show top N of max latency")
parser.add_argument("-i", "--interval", help="show latency interval")
parser.add_argument("-v", "--verbose", action="store_true", help="print more hists")
args = parser.parse_args()
topn = args.top
pid = args.pid
g_interval = args.interval
verbose = args.verbose
debug = 0


# load BPF program
b = BPF(src_file = "lat_v2.c")
b.attach_uprobe(name="/home/note/bcc/test", sym="func_test_lat", fn_name="do_entry")
b.attach_uretprobe(name="/home/note/bcc/test", sym="func_test_lat", fn_name="do_return")

# header
print("Tracing... Hit Ctrl-C to end.")


def main():
    # print("%-16s %-6s %-32s %-16s %-16s %-16s %-16s %-16s\n" % ("COMM", "PID", "API", "MIN", "MAX", "COUNT", "SUM", "AVG"))
    if g_interval:
        interval = g_interval
    else:
        interval = 999999999

    do_exit = 0
    while (1):

        try:
            sleep(interval)
        except KeyboardInterrupt:
            pass; do_exit = 1

        print("==\n")
        if (verbose):
            #b["dist"].print_log2_hist("usecs")
            b["dist"].clear()


        print("%-16s %-6s %-32s %-16s %-16s %-16s %-16s %-16s" % ("COMM", "PID", "API", "MIN", "MAX", "COUNT", "SUM", "AVG"))

        status = b.get_table("status")
        i = topn
        for k, v in sorted(status.items(), key=lambda status: status[1].max, reverse=True):
            i = i - 1
            if topn and i <= 0:
                break
            print("%-16s %-6s %-32s %-16s %-16s %-16s %-16s %-16d" 
                    % (k.comm, k.pid, k.api, v.min, v.max, v.count, v.sum, v.sum / v.count))        
        
        if do_exit:
            exit()
   

if __name__ == '__main__':
    main()
