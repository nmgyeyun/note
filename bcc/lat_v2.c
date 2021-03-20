/*
 * vfsreadlat.c		VFS read latency distribution.
 *			For Linux, uses BCC, eBPF. See .py file.
 *
 * Copyright (c) 2013-2015 PLUMgrid, http://plumgrid.com
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of version 2 of the GNU General Public
 * License as published by the Free Software Foundation.
 *
 * 15-Aug-2015	Brendan Gregg	Created this.
 */

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

