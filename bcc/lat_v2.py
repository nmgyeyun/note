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

def usage():
	print("USAGE: %s [interval [count]]" % argv[0])
	exit()

# arguments
interval = 5
count = -1
if len(argv) > 1:
	try:
		interval = int(argv[1])
		if interval == 0:
			raise
		if len(argv) > 2:
			count = int(argv[2])
	except:	# also catches -h, --help
		usage()

# load BPF program
b = BPF(src_file = "lat_v2.c")
b.attach_uprobe(name="/home/note/bcc/test", sym="func_test_lat", fn_name="do_entry")
b.attach_uretprobe(name="/home/note/bcc/test", sym="func_test_lat", fn_name="do_return")

# header
print("Tracing... Hit Ctrl-C to end.")

def main():
    # print("%-16s %-6s %-32s %-16s %-16s %-16s %-16s %-16s\n" % ("COMM", "PID", "API", "MIN", "MAX", "COUNT", "SUM", "AVG"))

    loop = 0
    do_exit = 0
    while (1):
        if count > 0:
            loop += 1
            if loop > count:
                exit()
        try:
            sleep(interval)
        except KeyboardInterrupt:
            pass; do_exit = 1
    
        print("==\n")
        #b["dist"].print_log2_hist("usecs")
        b["dist"].clear()

        status = b.get_table("status")

        # for k, v in status.items():
        #     print("%-16s %-6s %-32s %-16s %-16s %-16s %-16s %-16d" % (k.comm, k.pid, k.api, v.min, v.max, v.count, v.sum, v.sum / v.count))        

        print("%-16s %-6s %-32s %-16s %-16s %-16s %-16s %-16s" % ("COMM", "PID", "API", "MIN", "MAX", "COUNT", "SUM", "AVG"))

        for k, v in sorted(status.items(), key=lambda status: status[1].max, reverse=True):
            print("%-16s %-6s %-32s %-16s %-16s %-16s %-16s %-16d" 
                    % (k.comm, k.pid, k.api, v.min, v.max, v.count, v.sum, v.sum / v.count))        
        
        if do_exit:
            exit()
    


if __name__ == '__main__':
  # fire.Fire()
  main()
