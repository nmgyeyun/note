#!/usr/bin/python3
#

from __future__ import print_function
from bcc import BPF
from ctypes import c_ushort, c_int, c_ulonglong
from time import sleep
from sys import argv
import argparse

bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>


struct key_t {
    u64 ts;
    u32 pid;
    char comm[TASK_COMM_LEN];
    char api[64];    
};

struct value_t {
    u64 min;
	u64 max;
	u64 sum;
	u64 count;
};


BPF_HASH(status, struct key_t, struct value_t);
BPF_HASH(start, u32, struct key_t);
BPF_HISTOGRAM(dist);

int do_entry(struct pt_regs *ctx)
{
    u32 pid;        
    struct key_t val = {};    
    
    pid = bpf_get_current_pid_tgid();
    FILTER

    val.pid = pid;
    val.ts = bpf_ktime_get_ns();
    bpf_get_current_comm(&val.comm, sizeof(val.comm));
    bpf_probe_read_user(&val.api, sizeof(val.api), (void *)PT_REGS_PARM1(ctx));

    start.update(&pid, &val);

    return 0;
}

int do_return(struct pt_regs *ctx)
{
	u32 pid;
	u64 delta;
	struct key_t key = {}, *p_key;
	struct value_t val = {}, *p_val;

	pid = bpf_get_current_pid_tgid();
    FILTER

	p_key = start.lookup(&pid);
    if (!p_key) {
        return 0;
    }

	delta = (bpf_ktime_get_ns() - p_key->ts) / 1000;
	dist.increment(bpf_log2l(delta));

    key = *p_key;
    key.ts = 0;
	p_val = status.lookup(&key);
	if (p_val) {

		p_val->count += 1;
		p_val->sum += delta;
		p_val->min = delta;
		if (delta > p_val->max) {
			p_val->max = delta;
		}
		if (delta < val.min) {
			p_val->min = delta;
		}			
		status.update(&key, p_val);
	} else {
		val.count = 1;
		val.sum = delta;
		val.min = delta;
		val.max = delta;

		status.insert(&key, &val);
	}

	start.delete(&pid);

	return 0;
}
"""


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
parser.add_argument("-v", "--verbose", action="store_true", help="print latency distribution")
parser.add_argument("-d", "--debug", action="store_true", help="print debug info")
args = parser.parse_args()
topn = args.top
pid = args.pid
interval = args.interval
verbose = args.verbose

if args.top:
    topn = int(args.top)
else:
    topn = 0

if args.interval:
    interval = int(args.interval)
else:
    interval = 999999999


if args.pid:
    bpf_text = bpf_text.replace('FILTER',
        'if (pid != %s) { return 0; }' % args.pid)
else:
    bpf_text = bpf_text.replace('FILTER', '')

if args.debug:
    print(bpf_text)
    print("topn %s interval %s pid %s" % (topn, interval, pid))

# load BPF program
#b = BPF(src_file = "lat_v2.c")
b = BPF(text=bpf_text)
b.attach_uprobe(name="/home/note/bcc/test", sym="func_test_lat", fn_name="do_entry")
b.attach_uretprobe(name="/home/note/bcc/test", sym="func_test_lat", fn_name="do_return")
if args.debug:
    print(bpf_text)

# header
print("Tracing... Hit Ctrl-C to end.")


def main():
    do_exit = 0
    while (1):

        try:
            sleep(interval)
        except KeyboardInterrupt:
            pass; do_exit = 1

        if (verbose):
            #b["dist"].print_log2_hist("usecs")
            b["dist"].clear()


        print("%-16s %-6s %-32s %-16s %-16s %-16s %-16s %-16s" % ("COMM", "PID", "API", "MIN", "MAX", "COUNT", "SUM", "AVG"))

        status = b.get_table("status")
        i = topn
        for k, v in sorted(status.items(), key=lambda status: status[1].max, reverse=True):
            i = i - 1
            if topn and i < 0:
                break
            print("%-16s %-6s %-32s %-16s %-16s %-16s %-16s %-16d" 
                    % (k.comm, k.pid, k.api, v.min, v.max, v.count, v.sum, v.sum / v.count))        
        
        if do_exit:
            exit()
   

if __name__ == '__main__':
    main()
